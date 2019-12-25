CREATE TABLE fixtures ( 
fixture_id INTEGER PRIMARY KEY, 
league_id INTEGER, 
event_date TEXT, 
round TEXT,
status TEXT,
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
username TEXT UNIQUE, 
hash TEXT 
, points INTEGER);

CREATE TABLE users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE, 
hash TEXT  ,
points INTEGER,
hash TEXT, 
choice_league INTEGER);
