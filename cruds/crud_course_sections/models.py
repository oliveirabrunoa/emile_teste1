from backend import db


class CourseSections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20))
    name = db.Column(db.String(50))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    course_section_period = db.Column(db.String(6))
