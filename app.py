import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import *

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
db = SQL("sqlite:///finance.db")
dbTransactions = SQL("sqlite:///transactions.db")




@app.route("/")
@login_required
def index():
    """Show upcoming fixtures"""

    user_id = session["user_id"]
    response = get_all_fixtures(754)

    return render_template("/index.html", response=response.json())


@app.route("/league", methods=["GET", "POST"])
@login_required
def league():
    if request.method == "GET":
        return render_template("league.html")
    
    


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return jsonify("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    elif request.method =="POST":

        stock_data = lookup(request.form.get("symbol"))
        if not stock_data:
            return apology("Sorry, we couldn't find anything for this symbol.")
        else:
            return render_template("quoted.html", stock = stock_data )


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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "GET":
        user_id = session["user_id"]
        #Fetch list of owned stocks and how many of them
        stocks = dbTransactions.execute("SELECT symbol, SUM(amountShares) FROM 'transactions'\
        WHERE idUser=:user_id GROUP BY symbol; ", user_id=user_id )
        for stock in stocks:
            lookup_data = lookup(stock['symbol'])
            stock['full_name'] = lookup_data['name']
        print(stocks)
        return render_template("sell.html", stocks=stocks)



    elif request.method == "POST":
        user_id = session["user_id"]
        symbol_to_sell, shares_to_sell = request.form.get("symbol"), request.form.get("shares")
        print(f"Received from FORM : {symbol_to_sell} x {shares_to_sell}.")
        if not lookup(symbol_to_sell):
            return apology(f"Sorry, couldn't find anything for this symbol.")
        elif int(shares_to_sell) < 1 :
            return apology("Please enter an positive integer for the number of stocks.")
        else:
            stock = lookup(symbol_to_sell)
            print (f"Request is valid.\nSelling {shares_to_sell} shares of {stock['name']}...")
            #checks users has that many stocks

            stocks = dbTransactions.execute("SELECT symbol, SUM(amountShares) FROM 'transactions'\
            WHERE idUser=:user_id GROUP BY symbol; ", user_id=user_id )
            for stock in stocks:
                if stock['symbol'] == symbol_to_sell:
                    if int(stock['SUM(amountShares)']) < int(shares_to_sell):
                        return apology("You don't have enough shares.")
                    else:
                        #perform the sell
                        market_price = lookup(symbol_to_sell)['price']
                        result = dbTransactions.execute("INSERT INTO transactions(idUser, symbol, amountShares, price, type) \
                        VALUES (:idUser, :symbol, :amountShares, :price, :type ) ;",\
                        idUser=session["user_id"], symbol=symbol_to_sell, amountShares= -int(shares_to_sell), price= market_price, type="SELL")
                        if not result:
                            return "Something went wrong."
                        else:

                            response = db.execute("SELECT cash from users WHERE id = :userID", userID=session["user_id"])
                            cash = response[0]['cash']
                            total_cost = float(market_price) * float(shares_to_sell)
                            cash_result = db.execute("UPDATE users SET cash=:remaining_cash WHERE id=:userID",\
                            remaining_cash=cash-total_cost, userID=session['user_id'])
                            if not cash_result:
                                return 'Oops, something went wrong.'
                            else:
                                return redirect("/")


        return apology("This is a POST request.")



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
