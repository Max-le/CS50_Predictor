import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
from datetime import datetime


def get_all_available(data_type):
    response = requests.get(
        f'https://api-football-v1.p.rapidapi.com/v2/{data_type}',
        headers={'X-RapidAPI-Key': '8e33daace6msh8340cfb73cef51ep140be9jsn36c8f3ff8135'}
    )
    return response
def get_league(league_id):
    response = requests.get(
        f"https://api-football-v1.p.rapidapi.com/v2/leagues/league/{league_id}",
        headers={'X-RapidAPI-Key': '8e33daace6msh8340cfb73cef51ep140be9jsn36c8f3ff8135'}
    )
    return response
def get_all_fixtures(league_id):
    date = datetime.today().strftime('%Y-%m-%d')
    response = requests.get(
        f"https://api-football-v1.p.rapidapi.com/v2/fixtures/league/{league_id}/{date}",
        headers={'X-RapidAPI-Key': '8e33daace6msh8340cfb73cef51ep140be9jsn36c8f3ff8135'}

    )
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
