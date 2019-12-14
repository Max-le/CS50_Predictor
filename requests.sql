-- SQLite
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