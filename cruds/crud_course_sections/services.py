from flask import Blueprint, jsonify, request
from . import models
from backend import db
from cruds.crud_users.models import Users
from cruds.crud_section_times.models import SectionTimes
import datetime
from sqlalchemy import and_, or_


course_sections = Blueprint("course_sections", __name__)


@course_sections.route('/course_sections', methods=['GET'])
def get_course_section():
    return jsonify(course_sections=[dict(id=course_section.id, code=course_section.code) for course_section in models.CourseSections.query.all()])


@course_sections.route('/course_section_details/<course_section_id>', methods=['GET'])
def course_section_details(course_section_id):
    if not models.CourseSections.query.get(course_section_id):
        return jsonify({'result': 'Não encontrado!'})

    course_section= models.CourseSections.query.get(course_section_id)
    return jsonify(course_section=dict(id=course_section.id))



''' Não utilizado no experimento
@course_sections.route('/course_sections_students/<course_section_id>', methods=['GET'])
def course_sections_students(course_section_id):
    course_section_students = CourseSectionStudents.query.filter_by(course_section_id=course_section_id,status=1)
    students = [Users.query.get(course_section_student.user_id) for course_section_student in course_section_students]
    return jsonify(students_course_section=[dict(id=student.id, email=student.email, image_path= student.image_path) for student in students])
'''
