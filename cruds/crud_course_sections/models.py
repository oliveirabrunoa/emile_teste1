from backend import db
from cruds.crud_courses.models import Courses


class CourseSections(db.Model):
    __tablename__ = 'course_sections'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20))
    name = db.Column(db.String(50))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    course_section_period = db.Column(db.String(6))
    section_times = db.relationship("SectionTimes", backref='course_section', lazy='dynamic')
