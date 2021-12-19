from datetime import datetime
from app import db


class User(db.Model):
    u_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), index=True, unique=True)
    fantasy_name = db.Column(db.String(100), index=True, unique=True)
    def __repr__(self):
        return '<User {}>'.format(self.user_name)


class trades_clean(db.Model):
    u_id = db.Column(db.Integer, primary_key=True)
    ticker1 = db.Column(db.String(140))
    trade_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    amount = db.Column(db.Integer)

    def __repr__(self):
        return '<ticker1 {}>'.format(self.ticker1)

class final_summary(db.Model):
    user_name = db.Column(db.String(140),primary_key=True)
    fantasy_name = db.Column(db.String(140))
    final_change = db.Column(db.Integer, index=True)
    fb = db.Column(db.Integer)

    def __repr__(self):
        return '<final_change {}>'.format(self.final_change)
