from flask import Blueprint, jsonify, request
from . import models
from backend import db


courses = Blueprint("courses", __name__)

@courses.route('/courses', methods=['GET'])
def get_courses():
    return jsonify(courses=[dict(id=course.id, code=course.code, name=course.name) for course in models.Courses.query.all()])

#Retorna detalhes de um curso
@courses.route('/course_details/<course_id>', methods=['GET'])
def course_details(course_id):

     course = models.Courses.query.get(course_id)
     return jsonify(course=[
     					dict(
	     						id=course.id,
	                            code=course.code,
	                            name=course.name,
	                            credits=course.credits,
	                            program_section=course.program_section,
	                            course_type_id=course.course_type_id
                            )])
