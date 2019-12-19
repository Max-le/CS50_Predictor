CREATE TABLE fixtures ( 
fixture_id INTEGER PRIMARY KEY, 
league_id INTEGER, 
event_date VARCHAR(255), 
round VARCHAR(255),
status VARCHAR(255),
venue TEXT, 
homeTeam BLOB, 
awayTeam BLOB, 
goalsHomeTeam INTEGER, 
goalsAwayTeam INTEGER, 
score BLOB
);

CREATE TABLE bets (
bet_id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
fixture_id INTEGER NOT NULL,
guess_score BLOB,
final_score BLOB,
match_finished INTEGER);
CREATE TABLE users_copy (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username varchar(255) UNIQUE, 
hash varchar(255) 
, points INTEGER);

CREATE TABLE users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username varchar(255) UNIQUE, 
hash varchar(255)  ,
points INTEGER, hash TEXT);
