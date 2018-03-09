from flask import Blueprint, jsonify, request
from . import models
from backend import db


courses = Blueprint("courses", __name__)


@courses.route('/courses', methods=['GET'])
def get_courses():
    return jsonify(courses=[serializer.CoursesSerializer().serialize([course]) for course in models.Courses.query.all()])


@courses.route('/course_details/<course_id>', methods=['GET'])
def course_details(course_id):
    course = models.Courses.query.get(course_id)
    return jsonify(course=serializer.CoursesSerializer().serialize([course]))
