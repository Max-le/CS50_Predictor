# Predictor

 *Try to guess the outcome of soccer events and earn points for your right predictions !*

## Description

 This is my final project for the online course CS50's Introduction to Computer Science.

 This is basically like a betting website, but instead of betting ( and losing ) your money, you just earn points for correct decisions.

 As the CS50 Finance assignement, the project uses the web-framework [Flask](https://www.palletsprojects.com/p/flask/). 

Data used on this project is provided [API-Football.com](https://www.api-football.com/documentation).

### Features

* Place a bet on a upcoming fixture : try to guess the final score of the match.
* Once the match is finished, the server checks your prediction with the final score. : 
  - You get 3 points if you predicted the exact score. 
  - You get 1 point if you're right about winning and losing team or if you predicted a draw, but not the right number of goals.
  - Otherwise, you don't get points for the match. 
If the user predicted a draw ( but not the right # of goals ) : +1
The database are refreshed every 30 minutes.
* See the your activity on the page "My bets". 


## Installation


### Prerequisites
1. You need Python on your machine to work in this project : [Get Python](https://www.python.org/downloads/). ( I was using Python 3, not sure if it is important to use v.3 instead of v.2 )
2. CS50's library is used for this project. Install it by typing in terminal : 

  `pip3 install CS50`
  
3. The database is not included on this repository : you need to create one.
    1. The database system is SQLite3. Make sure it is installed on your machine. 
    Type `touch predictor.db` in Terminal on root directory of the project.

    The database's name has to be "predictor.db". ( You can change that, but then you'll also need to edit the source code )
    2. The database has three tables : Fixtures ( list all the events ), Bets ( all users predictions), and Users ( list of all users registered )
    The instructions to create thoses tables are provided in the "init_db.sql" file, so you can run it : 
    
    `sqlite3 predictor.db`
    
    Then

    `.read init_db.sql`




## Roadmap
Ideas for further development of the project :

* More standard registration : require email adress and minimum complexity for password. 
* More social predictions : compare your total score and predictions with your friends.