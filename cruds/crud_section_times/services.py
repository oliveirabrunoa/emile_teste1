from flask import Blueprint, jsonify, request
from . import models
from backend import db
from cruds.crud_course_sections.models import CourseSections
from cruds.crud_users.models import Users
from cruds.crud_courses.models import Courses
from cruds.crud_program.models import Program
from cruds.crud_institution.models import Institution
import pytz
import datetime
from sqlalchemy import and_


section_times = Blueprint("section_times", __name__)


@section_times.route('/section_times', methods=['GET'])
def get_section_times():
    return jsonify(section_times=[dict(id=section_time.id, course_section_id=section_time.course_section_id,
                                       week_day=section_time.week_day,
                                       section_time_start_time=str(section_time.section_time_start_time),
                                       section_time_finish_time=str(section_time.section_time_finish_time))
                                  for section_time in models.SectionTimes.query.all() ])

@section_times.route('/teachers_section_times/<teacher_id>', methods=['GET'])
def teachers_section_times(teacher_id):
    section_times = (db.session.query(models.SectionTimes).filter(Institution.id==Program.institution_id).
                                                            filter(Program.id==Courses.program_id).
                                                            filter(Courses.id==CourseSections.course_id).
                                                            filter(models.SectionTimes.course_section_id == CourseSections.id).
                                                            filter(CourseSections.teacher_id == teacher_id).
                                                            filter(CourseSections.course_section_period == Institution.current_program_section).all())

    return jsonify(section_times=[dict(id=section_time.id, course_section_id=section_time.course_section_id,
                                       week_day=section_time.week_day,
                                       section_time_start_time=str(section_time.section_time_start_time),
                                       section_time_finish_time=str(section_time.section_time_finish_time)) for section_time in section_times])

''' Não utilizado no experimento
@section_times.route('/section_time_in_progress/<teacher_id>', methods=['GET'])
def section_time_in_progress(teacher_id):
    now = datetime.datetime.now(tz=pytz.timezone('America/Bahia')).time()
    section_times = (db.session.query(models.SectionTimes).
                       filter(Institution.id==Program.institution_id).
                       filter(Program.id==Courses.program_id).
                       filter(Courses.id==CourseSections.course_id).
                       filter(Users.id == CourseSections.teacher_id).
                       filter(CourseSections.id == models.SectionTimes.course_section_id).
                       filter(Users.id == teacher_id).
                       filter(and_(models.SectionTimes.section_time_start_time <= now, models.SectionTimes.section_time_finish_time >= now)).
                       filter(models.SectionTimes.week_day == datetime.datetime.now(tz=pytz.timezone('America/Bahia')).weekday()).
                       filter(CourseSections.course_section_period == Institution.current_program_section).all())

    section_times_list = serializer.SectionTimeSerializer().serialize(section_times)
    return jsonify(section_times=section_times_list)


@section_times.route('/student_attendance_register/<course_section_id>', methods=['POST'])
def student_attendance_register(course_section_id):
    student_attendance_list = request.get_json()['student_attendance']
    section_time_date = request.get_json()['section_time_date']

    section_time = models.SectionTimes.query.filter_by(week_day=datetime.datetime.strptime(section_time_date, "%m-%d-%Y").date().weekday(), course_section_id=course_section_id).first()

    if not section_time:
        return jsonify(result="Invalid request - Section time not found"), 404

    student_attendance_registered = StudentAttendance.query.filter_by(section_time_date=datetime.datetime.strptime(section_time_date, "%m-%d-%Y").date()).all()
    if student_attendance_registered:
        return jsonify(result="Section time already registered"), 400

    try:
        with db.session.no_autoflush:
            for register in student_attendance_list:
                student_attendance = StudentAttendance(status=register['status'], section_time_date=datetime.datetime.strptime(section_time_date, "%m-%d-%Y").date())
                student_attendance.course_section_student_id = CourseSectionStudents.query.filter_by(user_id=register['student_id'],course_section_id=course_section_id).first().id
                section_time.student_attendance.append(student_attendance)

        db.session.commit()
        student_attendance_serialized = StudentAttendanceSerializer().serialize(section_time.student_attendance)
        return jsonify(student_attendance=student_attendance_serialized), 200
    except:
        return jsonify(result="Invalid request"), 404

'''

# @section_times.route('/update_section_time/<section_time_id>', methods=['POST'])
# def update_section_time(section_time_id):
#     section_time = models.SectionTimes.query.get(section_time_id)
#
#     if section_time:
#         section_time.set_fields(dict(request.form.items()))
#         db.session.commit()
#         return jsonify(section_time=[section_time.serialize() for section_time in models.SectionTimes.query.filter_by(id=section_time_id)])
#     return jsonify(result='invalid section time id')
