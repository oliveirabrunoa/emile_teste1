from backend import db
from cruds.crud_course_type.models import CourseType


class Courses(db.Model):

	id = db.Column(db.Integer, primary_key = True)
	code = db.Column(db.String(200))
	name = db.Column(db.String(500))
	credits = db.Column(db.Integer)
	hours = db.Column(db.Integer)
	program_section = db.Column(db.Integer)
	course_type_id = db.Column(db.Integer, db.ForeignKey('course_type.id'))
	program_id = db.Column(db.Integer, db.ForeignKey('program.id'))