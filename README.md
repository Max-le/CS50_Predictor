# Predictor

 *Try to guess the outcome of soccer events and earn points for your right predictions !*

The project is deployed on Heroku : http://predictor-foot.herokuapp.com/
## Description

 This is my final project for the online course CS50's Introduction to Computer Science.

 This is basically like a betting website, but instead of betting ( and losing ) your money, you just earn points for correct decisions.


As the CS50 Finance assignement, the project uses the web-framework [Flask](https://www.palletsprojects.com/p/flask/). 

Data used on this project is provided [API-Football.com](https://www.api-football.com/documentation).

#### Technical aspects : 
I didn't change much the file organization of this project from CS50 Finance : 
- app.py contains the "main" code : it is executed when running `flask run`. It contains all the routes and thus handles HTTP requests. 
- HTML Pages are in /templates folder. CSS and favicon.ico are in /static folder. 
- helpers.py holds functions that I wanted to externalize from app.py and functions already written by CS50 ( like the meme apology ).
- I created helpers_test.py to test several important functions ( unittest library ). 

I published a diagram that I used as a blueprint for the architecture of the code : [check it out here if you want](https://www.draw.io/?lightbox=1&highlight=0000ff&nav=1&title=Predictor%20Architecture.drawio#Uhttps%3A%2F%2Fdrive.google.com%2Fuc%3Fid%3D1dYA1t9bzluw2TpN6wMd3xZD8H4PFihyt%26export%3Ddownload).

### Features

* Place a bet on a upcoming fixture : try to guess the final score of the match. The homepage ( index.html ) shows several upcoming matches for a football championship. 

* Once the match is finished, the server checks your prediction with the final score. : 
  - You get 3 points if you predicted the exact score. 
  - You get 1 point if you're right about winning and losing team or if you predicted a draw, but not the right number of goals.
  - Otherwise, you don't get points for the match. 
If the user predicted a draw ( but not the right # of goals ) : +1

The table in the database containing all the informations about fixtures is refreshed every 30 minutes.
* See the your activity on the page "My bets". 


## Installation

First of all, you should obviously download the project of your machine. 
You need an account on [API-Football.com](https://www.api-football.com/documentation) in order to get an **API key**. ( basic account is free ).
  The code reads the API key from a external file named "api.key", so once you managed to get your key in API-Football.com, create a file named "api.key" ( .key is the extension ). In Terminal, you can navigate to the directory and type 

  `touch api.key`

Open the file and paste your key in the file, just plain text, no quote. 


1. You need Python on your machine to work in this project : [Get Python](https://www.python.org/downloads/). ( I was using Python 3, not sure if it is important to use v.3 instead of v.2 )
2. Install Flask. CS50's library is also used for this project ( for connecting with the database ). Install it all by typing in terminal : 

  `pip3 install CS50 Flask Flask-session requests`

  
3. The database is not included on this repository : you need to create one.
    The database system is SQLite3. Make sure it is installed on your machine. 

    Type 
    
    `touch predictor.db` 
    
     Terminal on root directory of the project.

    The database's name has to be "predictor.db". ( You can change that, but then you'll also need to edit the source code ).

    The database has three tables : Fixtures ( list all the events ), Bets ( all users predictions), and Users ( list of all users registered )
    The instructions to create thoses tables are provided in the "init_db.sql" file, so you can run it : 

    Type in terminal : 
    
    `sqlite3 predictor.db`
    
    Then

    `.read init_db.sql`

    Press <kbd>Ctrl</kbd> + <kbd>D</kbd> to exit Sqlite. 


## Usage
Once everyting's installed : 

Type 

` flask run `

 on a terminal window,  it will execute app.py and start the server.
To make the server visible on all local network : 

```flask run --host=0.0.0.0```

Port 5000 by default, so access in web browser locally using : 

http://localhost:5000/

Create an account on http://localhost:5000/register. 

The first time you run the server, you may see an empty table on the home page.  That's normal, the database you created is empty. You need to update the database manually.
I made a function in helpers.py that fetchs the data via an API Call and add and updates the Fixtures table. 
You can call it via a query string in the route /update_fixtures with the ID of the league as a argument. For example locally that would be : 

http://localhost:5000/update_fixtures?id=525

Here's a few IDs of the leagues available on API-Football.com : 

754= Current Bundesliga, 656=Current Pro League, 525=Ligue 1, 524 = England Premier League

Of course, the full list can be retrieved using an API Call to their service. 

## Roadmap
Ideas for further development of the project :

* More standard registration : require email adress and minimum complexity for password, not just a username. 
* More social : compare your total score and predictions with your friends.
  * Invite friends to join ( send email )
  * Create parties and rank users. 
* Ability to switch leagues