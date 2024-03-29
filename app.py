import os

#from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session

from flask_sqlalchemy import SQLAlchemy

from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import *
import datetime
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from flask_migrate import Migrate



##754= Current Bundesliga, 656=Current Pro League, 525=Ligue 1
LEAGUES_AVAILABLE = [525, 754, 514, 656, 524]


# Configure application
app = Flask(__name__)

# Database options
HEROKU_URI = "postgresql://qvjmykpceknmbn:5b270002260d794ef0915621c4536ac23fd6573846eb6af4758439e618d75f98@ec2-46-137-188-105.eu-west-1.compute.amazonaws.com:5432/d5b9cc76c67ea8"
LOCAL_URI = "postgresql://max@localhost:5432/max"
SQLITE_DB = 'sqlite:///predictor.db'


# app.config['SQLALCHEMY_DATABASE_URL'] = os.environ["DATABASE_URL"]
app.config['SQLALCHEMY_DATABASE_URI'] = LOCAL_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


def update_job():
    '''This function is called on regular intervals by the BackgroundScheduler'''
    print('Scheduled Background job has started.')
    return 0 


scheduler = BackgroundScheduler()
scheduler.add_job(update_job, trigger='interval', minutes=30)
scheduler.start()
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached so we avoid unnoticed changes in the browser.
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


from models import User, Match, Bet


@app.route("/")
@login_required
def index():
    """Show upcoming fixtures"""
    username = session["username"]
    now = datetime.datetime.strftime(datetime.datetime.today(), "%Y-%m-%dT%H:%M:%S%z")
    fixtures = Match.query.all()
    
    for f in fixtures: 
        print(f.team_home, f.team_away)
        #place_teams_logo(f)
        #replace_teams_names(f)
        if f.time : f.time = prettier_time(f.time) #Formats date for better displaying
    return render_template("/index.html", fixtures=fixtures)

@app.route('/leagues')  
def leagues():
    f = open("models/leagues.json", "r")
    leagues = json.loads(f.read())
    return render_template("leagues.html", leagues=leagues['api']['leagues'])

@app.route('/choose_your_league', methods=['GET', 'POST'])
@login_required
def choose_your_league():
    if request.method == 'POST':
        choice = request.form.get("l_choice")
        ##Save choice in db and in session
        session['l_choice'] = choice
        result = db.execute("UPDATE users SET choice_league=:choice WHERE id=:u_id ", choice=choice, u_id=session['user_id'])
        if not result: 
            return f"Error : couldn't save choice in database for user {session['user_id']} "
        return f" Your choice : {choice} was saved !"
    elif request.method == 'GET':
        ##Loads leagues from json
        f = open('models/leagues.json', 'r')
        leagues = json.loads(f.read())['api']['leagues']
        n_leagues = []
        for l in leagues: 
            if l['league_id'] in LEAGUES_AVAILABLE:
                n_leagues.append(l)
        return render_template("choose_your_league.html", leagues=n_leagues)
    return 0 

@app.route('/refresh_db', methods=['GET'])
@login_required   
def refresh_db():
    '''Update all fixtures of the league with the provided id.'''
    league_id = request.args.get('id')
    if not league_id :
        return "Please provide a league ID as URL string parameter."
    print('Updating fixtures table in database : adding league ', league_id)
    result = update_databse(league_id)
    update_final_scores()
    return f"{result} fields updated."

@app.route("/mybets")
@login_required

def mybets():
    u_id = session["user_id"]
    bets = db.execute("SELECT * FROM bets WHERE user_id=:user_id", user_id=u_id)
    update_final_scores()
    assign_user_score(u_id, calculate_score(u_id))
    if not bytes:
        return apology('Something went wrong with the SQL query.')
    for bet in bets: 
        id = bet["fixture_id"]
        bet["homeTeam"] = home_team_name(id)
        bet["awayTeam"] = away_team_name(id)
        bet["event_date"] = get_event_date(id)
        bet["event_date"] = prettier_time(bet["event_date"])
    
    return render_template("mybets.html", bets=bets, points=get_user_points(u_id))
@app.route("/past_fixtures")
@login_required
def past_fixtures():
    """Show past fixtures"""
    user_id = session["user_id"]
    fixtures = db.execute("SELECT fixture_id, event_date, venue, homeTeam, awayTeam FROM fixtures ")    
    print("Type : ", type(fixtures))
    pastF = []
    for f in fixtures: 
        replace_teams_names(f) 
        date_event = datetime.datetime.strptime(f['event_date'], "%Y-%m-%dT%H:%M:%S%z")
        #filter out past fixtures
        if date_event.replace(tzinfo=None) < datetime.datetime.today():
            pastF.append(f)

    return render_template("/index.html", fixtures=pastF)
@app.route("/savebet", methods=["POST"])
@login_required
def savebet():
    '''Save a bet (received via POST) to the database'''
    home_score, away_score = request.form.get('home_score'), request.form.get('away_score')
    id = request.form.get('fixture_id')
    guess_score=f"{str(home_score)} - {str(away_score)}"#formats score for database
    #check if there's no bet placed yet for this fixture
    check_bet = db.execute("SELECT * FROM bets WHERE fixture_id = :id", id=id)
    if check_bet:
        return f"Sorry, you alreay placed a bet for this event.\n\n {check_bet}"
    result = db.execute("INSERT INTO bets (user_id, fixture_id, guess_score)\
        VALUES (:user_id , :fixture_id , :guess_score)",\
        user_id=session["user_id"], fixture_id=id, guess_score=guess_score )
    print(f"Score received : {guess_score} id : {id}. Result query : {result}")
    return redirect("/mybets")


@app.route("/placebet", methods=["GET", "POST"])
@login_required
def placebet():
    '''Allows the use to create a bet on a fixture'''
    if request.method == "GET":
        return "Only use this route with POST request from the home page."
    if request.method == "POST":
        result = db.execute("SELECT fixture_id, event_date, venue, homeTeam, awayTeam from fixtures WHERE fixture_id=:id", id=request.form.get('id'))
        if not result:
            return apology("Sorry, something went wrong.")
        awayTeam_name = json.loads(result[0]["awayTeam"])["team_name"]
        homeTeam_name = json.loads(result[0]["homeTeam"])["team_name"]
        venue = result[0]["venue"]
        fixture_id = result[0]["fixture_id"]
        event_date = prettier_time(result[0]['event_date'])
        return render_template("placebet.html", awayTeam_name=awayTeam_name, homeTeam_name=homeTeam_name,\
        venue=venue, event_date=event_date, fixture_id=fixture_id)



@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return jsonify("TODO")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # try to find the provided username is the db
        user = User.query.filter_by(username=request.form.get("username")).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password_hash, request.form.get('password')):
            flash('Please check your login details and try again.')
            return 'error login' # if the user doesn't exist or password is wrong, reload the page
        print(user)
        # Remember which user has logged in
        session["username"] = user.username
        print("sesssion created : ", session["username"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        print('Returning login form')
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("enter your username !", 400)
        elif not request.form.get("password") or not request.form.get("confirmation"):
            return apology("enter your password and password confirmation !", 400)
        ##Checks password and confirmation are the same
        if request.form.get("password") == request.form.get("confirmation"):

            if (User.query.filter_by(username=request.form.get('username'))):
                print("username already exists.")


            pwdhash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
            print("Hash : ", pwdhash)

            ## the query may fail if username is already in the DB.
            new_user = User(username=request.form.get("username"), password_hash=pwdhash)
            db.session.add(new_user)
            db.session.commit()
            print("Successfully created user.\n ")
            return render_template("success.html")

        else:
            return apology("Password and its confirmation are not identical.", 400)

    elif request.method == "GET":
        return render_template("register.html")
    else:
        return apology(f"{request.method} ? What kind of request is that ?")



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
