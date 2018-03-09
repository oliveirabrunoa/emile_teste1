from flask import Blueprint, jsonify, request
from . import models
from backend import db


courses = Blueprint("courses", __name__)


@courses.route('/courses', methods=['GET'])
def get_courses():
    return jsonify(courses=[dict(id=course.id) for course in models.Courses.query.all()])


@courses.route('/course_details/<course_id>', methods=['GET'])
def course_details(course_id):
    return jsonify(course=[dict(id=course.id) for course in models.Courses.query.filter_by(id=course_id).all()])
