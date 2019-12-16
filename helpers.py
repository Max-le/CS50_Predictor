import os, json
import requests
import urllib.parse
from cs50 import SQL
from flask import redirect, render_template, request, session
from functools import wraps
from datetime import datetime, timedelta

db = SQL("sqlite:///predictor.db")


def update_fixtures_database():
    '''Performs an API Call and update Fixtures database accordingly'''
    response_data = get_fixtures_league(754).json() ##754= Current Bundesliga, 656=Current Pro League
    fixtures = response_data["api"]["fixtures"]
    if not fixtures: 
        print("NO DATA FOUND.")
        return 1
    print(response_data["api"]["results"], "entries. ")
    count = 0 
    for fixture in fixtures: 
        result = db.execute("\
        INSERT INTO fixtures\
        (fixture_id,league_id,event_date,status, venue,\
        homeTeam,awayTeam, goalsHomeTeam, goalsAwayTeam, score\
        ) VALUES\
        (:fixture_id, :league_id, :event_date, :status,\
        :venue, :homeTeam, :awayTeam, :goalsHomeTeam, :goalsAwayTeam, :score);",\
        fixture_id=fixture["fixture_id"], league_id=fixture["league_id"], event_date=fixture["event_date"],\
        status=fixture["status"], venue=fixture["venue"], homeTeam=json.dumps(fixture["homeTeam"]), awayTeam=json.dumps(fixture["awayTeam"]),\
        goalsHomeTeam=fixture["goalsHomeTeam"], goalsAwayTeam=fixture["goalsHomeTeam"], score=json.dumps(fixture["score"]))
        if not result :
            ##Try UPDATE
            print(f"Couldn't write entry {fixture['fixture_id']}, it's likely it already exists.\nTrying UPDATE query... ")
            
            update_result = db.execute("UPDATE fixtures SET\
            event_date = :event_date, status = :status, venue = :venue,\
            goalsHomeTeam = :goalsHomeTeam, awayTeam = :awayTeam, homeTeam = :homeTeam,\
            goalsAwayTeam = :goalsAwayTeam, score = :score WHERE fixture_id = :fixture_id",\
            fixture_id=fixture["fixture_id"], event_date=fixture["event_date"],\
            status=fixture["status"], venue=fixture["venue"], homeTeam=json.dumps(fixture["homeTeam"]), awayTeam=json.dumps(fixture["awayTeam"]),\
            goalsHomeTeam=fixture["goalsHomeTeam"], goalsAwayTeam=fixture["goalsHomeTeam"], score=json.dumps(fixture["score"]))
            if not update_result: 
                print("UPDATE FAILED. SOMETHING WENT WRONG. ", update_result)
                return 2; 
            print("UPDATE Successfull : ", update_result)
        count+=1
        print("DB INSERT successfull:",result)
    print(count, "fields updated.")
    return count

def local_fixture_data(fixture_id):
    result = db.execute("SELECT * FROM fixtures WHERE fixture_id=:id", id=fixture_id)
    if not result:
        print("Warning : None result from SQL SELECT query")
        return None
    return result[0]
def home_team_name(fixture_id):
    f = local_fixture_data(fixture_id)
    if not f:
        raise Exception(f"Fixture {fixture_id} couldn't be found in the databse Fixtures.")
    return json.loads(f["homeTeam"])["team_name"]
def get_event_date(fixture_id):
    '''gets the event of a fixture from its ID.'''
    date = db.execute("SELECT event_date FROM fixtures WHERE fixture_id=:id", id=fixture_id)
    if not date:
        raise Exception(f"Fixture {fixture_id} couldn't be found in the databse Fixtures.") 
    return date[0]["event_date"] 


def away_team_name(fixture_id):
    f = local_fixture_data(fixture_id)
    if not f:
        raise Exception(f"Fixture {fixture_id} couldn't be found in the databse Fixtures.")
    return json.loads(f["awayTeam"])["team_name"]


def get_fixtures_league(league_id):
    ''''Makes an API call to get all knowns fixtures on the league '''
    response = requests.get(
        f"https://api-football-v1.p.rapidapi.com/v2/fixtures/league/{league_id}?timezone=Europe/Paris",
        headers={'X-RapidAPI-Key': '8e33daace6msh8340cfb73cef51ep140be9jsn36c8f3ff8135'}
    )
    print(f"{response.headers['X-RateLimit-requests-Remaining']} / {response.headers['X-RateLimit-requests-Limit']} API calls remaining for today." )
    return response
def replace_teams_names(fixture):
    # Replace homeTeam and awayTeam fields by a string 
    # containing only the name of the team instead of a JSON bundle. 
    teamH_name = json.loads(fixture["homeTeam"])["team_name"]
    teamA_name = json.loads(fixture["awayTeam"])["team_name"] 


    fixture["homeTeam"], fixture["awayTeam"] = teamH_name, teamA_name
    return 0 

def parse_scores(scores: str) -> list:
    '''Returns the score from string format '# - #' to list of two integers.'''
    l = []
    l.append(int(scores[0]))
    l.append(int(scores[len(scores) - 1]))
    return l
def calculate_score(user_id: int) -> int:
    '''returns the total score of a user from its ID'''
    bets = db.execute("SELECT * FROM bets WHERE user_id=:id", id = user_id)
    if not bets : 
        raise Exception(f"Error with query to Bets table using user_id =  {user_id} ")
    points = 0 
    for bet in bets:
        if bet["final_score"] != None :
            guess = parse_scores(bet["guess_score"])
            final = parse_scores(bet["final_score"])
            ##Perfect guess
            if guess[0] == final[0] and guess[1] == final[1]:
                points+=3
            ##correctly guess winning and losing teams or guess a draw, without the exact score
            elif (guess[0] > guess[1] and final[0] > final[1])\
                or (guess[0] < guess[1] and final[0] < final[1])\
                or (guess[0] == guess[1] and final[0 == final[1]]):
                points+=1
            else:
                points+=0
    return points

                


    return points
def update_final_scores():
    '''Updates the final_score field in Bets table from Fixtures table'''
    count = 0
    #Get all fixtures existing in Bets table 
    bets = db.execute("SELECT fixture_id FROM bets")
    for bet in bets: 
        fixture = db.execute("SELECT status, score FROM fixtures WHERE fixture_id=:id", id=bet["fixture_id"])
        match_status = fixture[0]["status"]
        if match_status == "Match Finished":
            update_result = db.execute("UPDATE bets SET final_score = :score, match_finished='True' WHERE fixture_id = :id ;")
            return 0 

    return 0 



    

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        response = requests.get(f"https://cloud-sse.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"
