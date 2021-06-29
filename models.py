from app import db
from sqlalchemy.dialects.postgresql import JSON


class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(80), primary_key=True, unique=True) # Primary key
    password_hash = db.Column(db.String(256), nullable=False)
    bets = db.relationship('Bet', backref='user', lazy=True)


    def __repr__(self):
        return '<id {}>'.format(self.username)


class Bet(db.Model): 
    __tablename__ = 'bets'

    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.String(512), nullable=False)
    username = db.Column(db.String(80), db.ForeignKey('users.username')) # Foreign key
    score_team_home = db.Column(db.Integer)
    score_team_away = db.Column(db.Integer)


    def __repr__(self):
        return '<id {}>'.format(self.id)



class Match(db.Model):
    __tablename__ = 'matches'


    id = db.Column(db.Integer, primary_key=True, unique=True)
    team_home = db.Column(db.String(128), nullable=False)
    team_away = db.Column(db.String(128), nullable=False)
    time = db.Column(db.DateTime())
    details = db.Column(db.String(512), nullable=False)


    def __repr__(self):
        return '<id {}>'.format(self.id)