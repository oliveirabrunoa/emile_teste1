from flask import Blueprint, jsonify, request
from . import models
from backend import db
from cruds.crud_courses.models import Courses
from cruds.crud_users.models import Users
from cruds.crud_course_sections.models import CourseSections
from sqlalchemy import and_, or_
from sqlalchemy import func
from cruds.crud_institution.models import Institution


program = Blueprint("program", __name__)

@program.route('/programs', methods=['GET'])
def programs():
    return jsonify(programs=[dict(id=program.id, name=program.name, abbreviation=program.abbreviation) for program in models.Program.query.all()])


#Retorna todas as aulas de um curso.
@program.route('/programs_course_sections/<program_id>', methods=['GET'])
def programs_course_sections(program_id):
    course_sections = (db.session.query(CourseSections).
                       filter(CourseSections.course_id==Courses.id).
                       filter(Courses.program_id==models.Program.id).
                       filter(models.Program.id==program_id).all())
    return jsonify(course_sections=[dict(id=course_section.id,
                                         code=course_section.code)
                                         for course_section in course_sections])





''' Não utilizado no experimento



@program.route('/programs_courses/<program_id>', methods=['GET'])
def programs_courses(program_id):
    program = models.Program.query.get(program_id)
    if not program:
        return jsonify(result="invalid program id"), 404
    return jsonify(program=program), 200




@program.route('/students_program_history/<student_id>', methods=['GET'])
def students_program_history(student_id):
    student = Users.query.get(student_id)
    program = models.Program.query.get(student.program_id)

    students_program_history_list = []

    if not student and student.type == 1:
        return jsonify(result="invalid student id"), 404

    hours_completed, credits_completed = program_current_progress(student)
    program_details = {"hours_completed":hours_completed, "credits_completed":credits_completed ,"total_credits": program.total_credits, "total_hours": program.total_hours}
    for course in program.courses:
        _dict = {"course": course}
        _dict.update(last_status_and_grade(course, student))
        times = course_times(course, student)
        _dict['times']= times

        students_program_history_list.append(_dict)

    return jsonify(students_program_history=[program_history for program_history in students_program_history_list], program= program_details)


@program.route('/update_coordinator/<program_id>/<coordinator_id>', methods=['POST'])
def update_coordinator(program_id, coordinator_id):
    coordinator = Users.query.get(coordinator_id)
    program = models.Program.query.get(program_id)

    if not program or not coordinator:
        return jsonify(result="invalid program or coordinator id"), 404
    if coordinator.type!=3:
        return jsonify(result="user is not a coordinator"), 400

    print(coordinator.id)
    program.coordinator_id = coordinator.id
    db.session.commit()

    return jsonify(program=program), 200


def course_times(course, student):
    course_aggregation = models.Program.manager.course_times_by_student(course, student)

    return course_aggregation[0] if course_aggregation else 0


def program_current_progress(student):
    return models.Program.manager.hours_and_credits_completed(student)


def last_status_and_grade(course, student):
    course_section_student = models.Program.manager.last_course_section_student(course, student)
    _dict = {}

    if not course_section_student:
        _dict['status'] = CourseSectionStudentsStatusSerializer().serialize([CourseSectionStudentsStatus.query.get(4)])
        _dict['grade']= 0
    else:
        _dict['status']= CourseSectionStudentsStatusSerializer().serialize([CourseSectionStudentsStatus.query.get(course_section_student.status)])
        _dict['grade']= course_section_student.grade
    return _dict
'''
