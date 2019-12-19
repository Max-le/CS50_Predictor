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

## Roadmap
Ideas for further development of the project :
* More social predictions : compare your total score and predictions with your friends.
* More standard registration : require email adress and minimum complexity for password. 