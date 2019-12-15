import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import *
import datetime
import requests
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached so we avoid unnoticed changes in the browser.
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///predictor.db")



@app.route("/")
@login_required
def index():
    """Show upcoming fixtures"""
    user_id = session["user_id"]
    fixtures = db.execute("SELECT fixture_id, event_date, venue, homeTeam, awayTeam FROM fixtures ")    
    print("Type : ", type(fixtures))
    upcoming_fixtures = []
    for f in fixtures: 
        replace_teams_names(f) 
        date_event = datetime.datetime.strptime(f['event_date'], "%Y-%m-%dT%H:%M:%S%z")
        #filter out past fixtures
        if date_event.replace(tzinfo=None) > datetime.datetime.today():
            upcoming_fixtures.append(f)

    return render_template("/index.html", fixtures=upcoming_fixtures)

    

@app.route('/update_database')  
@login_required
def update_database():
    result = update_fixtures_database()
    return f"{result} fields updated."

@app.route("/mybets")
@login_required
def mybets():
    bets = db.execute("SELECT * FROM bets WHERE user_id=:user_id", user_id=session['user_id'])
    if not bytes:
        return apology('Something went wrong with the SQL query.')
    for bet in bets: 
        bet["homeTeam"] = home_team_name(bet["fixture_id"])
        bet["awayTeam"] = away_team_name(bet["fixture_id"])
    return render_template("mybets.html", bets=bets)

@app.route("/savebet", methods=["POST"])
@login_required
def savebet():
    '''Save a bet (received via POST) to the database'''
    home_score, away_score = request.form.get('home_score'), request.form.get('away_score')
    if not home_score or not away_score:
        return apology("You didn\'t enter the score correctly. Please try again.", 400)
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
        event_date = datetime.datetime.strptime(result[0]['event_date'], "%Y-%m-%dT%H:%M:%S%z")
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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        print(session["user_id"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
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
            pwdhash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
            print("Hash : ", pwdhash)

            ## the query may fail if username is already in the DB.
            result = db.execute("INSERT INTO users  ( username, hash ) VALUES ( :username, :hash );"
            ,username=request.form.get("username"), hash=pwdhash )

            if not result:
                return apology(f"Sorry, we got an error code {result}. It's likely the username is already taken.")
            else:
                print("Successfully created user.\n ")
                session["user_id"] = result # execute() actually returns the id of the just-created value
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
