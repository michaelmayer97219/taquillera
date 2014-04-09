from app import db

movies = db.Table('movies',
	db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
	db.Column('location_id', db.Integer, db.ForeignKey('location.id'))
)

class Location(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	nickname = db.Column(db.String(64), index = True, unique = True)
	#address = db.Column(db.String(120), index = True, unique = True)
	#phonenumber = db.Column(db.String(64), index = True, unique = True)
	movies = db.relationship('Movie', secondary=movies, backref=db.backref('location', lazy='dynamic'))

	def __init__(self, nickname):
		self.nickname = nickname

	def __repr__(self, nickname):
		
		return self.nickname

class Movie(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120), index = True, unique = True)
	description = db.Column(db.Text, index = True)

	def __repr__(self):
		return self.title


