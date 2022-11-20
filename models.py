from init import db


class User(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name  = db.Column(db.String(100), nullable=False)
    password   = db.Column(db.String(100), nullable=False)
    login      = db.Column(db.String(80), unique=True, nullable=False)
    age        = db.Column(db.Integer)
    gender     = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.first_name}>'

class Message(db.Model):
    id               = db.Column(db.Integer, primary_key=True)
    owner_username   = db.Column(db.String(100), nullable=False)
    sender_username  = db.Column(db.String(100), nullable=False)
    status           = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.owner_username}>'

class Profile_Photo(db.Model):
	id               = db.Column(db.Integer, primary_key=True)
	photo_url        = db.Column(db.String(100), nullable=False)
	owner_username   = db.Column(db.String(100), nullable=False)