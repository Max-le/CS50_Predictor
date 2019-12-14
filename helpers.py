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
    response_data = get_fixtures_league(754).json()
    fixtures = response_data["api"]["fixtures"]
    if not fixtures: 
        print("NO DATA FOUND.")
        return 1
    print(response_data["api"]["results"], "entries. ")
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
            goalsHomeTeam = :goalsHomeTeam, goalsAwayTeam = :goalsAwayTeam, score = :score WHERE fixture_id = :fixture_id",\
            fixture_id=fixture["fixture_id"], event_date=fixture["event_date"],\
            status=fixture["status"], venue=fixture["venue"], homeTeam=json.dumps(fixture["homeTeam"]), awayTeam=json.dumps(fixture["awayTeam"]),\
            goalsHomeTeam=fixture["goalsHomeTeam"], goalsAwayTeam=fixture["goalsHomeTeam"], score=json.dumps(fixture["score"]))
            if not update_result: 
                print("UPDATE FAILED. SOMETHING WENT WRONG. ", update_result)
            print("UPDATE Successfull : ", update_result)
        print("DB INSERT successfull:",result)

def get_fixtures_league(league_id):
    response = requests.get(
        f"https://api-football-v1.p.rapidapi.com/v2/fixtures/league/{league_id}?timezone=Europe/Paris",
        headers={'X-RapidAPI-Key': '8e33daace6msh8340cfb73cef51ep140be9jsn36c8f3ff8135'}

    )
    print(f"{response.headers['X-RateLimit-requests-Remaining']} / {response.headers['X-RateLimit-requests-Limit']} API calls remaining for today." )
    return response

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
