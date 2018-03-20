from backend import db


class Program(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	abbreviation = db.Column(db.String(10))
	total_hours = db.Column(db.Integer)
	total_credits = db.Column(db.Integer)
	intitution_id = db.Column(db.Integer, db.ForeignKey('institution.id'))