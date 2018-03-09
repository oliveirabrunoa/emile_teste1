from flask import Blueprint, jsonify, request
from . import models
from backend import db


courses = Blueprint("courses", __name__)

#Retorna todos os cursos
@courses.route('/courses', methods=['GET'])
def get_courses():
    pass

#Retorna detalhes de um curso
@courses.route('/course_details/<course_id>', methods=['GET'])
def course_details(course_id):
    pass
