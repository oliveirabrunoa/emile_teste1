from flask import jsonify, Blueprint, request, url_for, send_from_directory
from . import models
from backend import db
from cruds.crud_course_sections.models import CourseSections
from cruds.crud_program.models import Program
from cruds.crud_courses.models import Courses
from cruds.crud_institution.models import Institution
from cruds.crud_users.models import Users
import os
from werkzeug.utils import secure_filename
import settings
from cruds.crud_user_type.models import UserType


users = Blueprint("user", __name__)


@users.route('/users', methods=['GET'])
def get_users():
    return jsonify(users=[dict(id=user.id, email=user.email) for user in models.Users.query.all()])


@users.route('/students', methods=['GET'])
def get_students():
    return jsonify(users=[dict(id=user.id, email=user.email) for user in models.Users.query.filter_by(type=1)])


@users.route('/teachers', methods=['GET'])
def get_teachers():
    return jsonify(users=[dict(id=user.id, email=user.email) for user in models.Users.query.filter_by(type=2)])





''' Não utilizado no experimento
@users.route('/add_student', methods=['POST'])
def add_student():
    data = dict(request.get_json())

    user = models.Users()
    user.set_fields(dict(username=None, gender=None, address=None,birth_date=None,name=data.get('name'),email=data.get('email'), program_id=data.get('program_id'), type=1))
    user.set_password(data.get('password'))
    db.session.add(user)

    course_sections_ids = data.get('course_sections')
    if course_sections_ids:
        save_course_sections(user, course_sections_ids)

    user = models.Users.query.filter_by(email=user.email).first()
    user_serialized = serializer.UsersSerializer().serialize([user])

    return jsonify(user=user_serialized), 200

def save_course_sections(user, course_sections_ids):
    with db.session.no_autoflush:
        for course_sections_id in course_sections_ids:
            course_section = CourseSections.query.get(course_sections_id)
            course_section_students = CourseSectionStudents(grade=0, status=1)
            course_section_students.course_section = course_section
            user.course_sections.append(course_section_students)
    db.session.commit()

@users.route('/user_details/<user_param>', methods=['GET'])
def user_details(user_param):
    user = None
    if str(user_param).isdigit():
        user = models.Users.query.get(user_param)
    else:
        user = models.Users.query.filter_by(email=user_param).first()

    if not user:
        return jsonify(result='Invalid user parameter'), 404

    user_serialized = serializer.UsersSerializer().serialize([user])
    return jsonify(user=user_serialized), 200


@users.route('/update_user/<user_id>', methods=['POST'])
def update_user(user_id):
    data = dict(request.get_json())
    user = models.Users.query.get(user_id)

    if user:
        user.set_fields(data)

        course_sections_ids = data.get('course_sections')
        if course_sections_ids:
            delete_course_sections(user)
            save_course_sections(user,course_sections_ids)

        user_serialized = serializer.UsersSerializer().serialize([user])
        db.session.commit()
        return jsonify(user=user_serialized)

    return jsonify(result='invalid user id')


@users.route('/update_password/<user_id>', methods=['POST'])
def update_password(user_id):
    data = dict(request.get_json())
    user = models.Users.query.get(user_id)

    if not user:
        return jsonify(result='invalid user id'), 404

    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not user.check_password(old_password):
        return jsonify(result='invalid password'), 400

    user.set_password(new_password)
    db.session.commit()
    user_serialized = serializer.UsersSerializer().serialize([user])

    return jsonify(user=user_serialized)

def delete_course_sections(user):
    (db.session.query(CourseSectionStudents).filter(CourseSectionStudents.user_id==user.id)
                                        .filter(CourseSectionStudents.status==1).delete())
    db.session.commit()


@users.route('/delete_user/<user_id>', methods=['POST'])
def delete_user(user_id):
    user = models.Users.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(users="Deleted user successfully")
    return jsonify(result='invalid user id')


@users.route('/teachers_course_sections/<user_id>', methods=['GET'])
def teachers_course_sections(user_id):
    user = models.Users.query.filter_by(id=user_id).first()

    if not user:
        return jsonify(result='invalid user id')

    course_sections = []
    if user.type==2:
        course_sections = (db.session.query(CourseSections).
                                    filter(Institution.id==Program.institution_id).
                                    filter(Program.id==Courses.program_id).
                                    filter(Courses.id==CourseSections.course_id).
                                    filter(CourseSections.teacher_id==user_id).
                                    filter(CourseSections.course_section_period==Institution.current_program_section).all())
    elif user.type==3:
        course_sections = (db.session.query(CourseSections).
                                    filter(Institution.id==Program.institution_id).
                                    filter(Program.id==Courses.program_id).
                                    filter(Courses.id==CourseSections.course_id).
                                    filter(CourseSections.course_section_period==Institution.current_program_section).
                                    filter(Program.id==user.program_id).all())

    return jsonify(teachers_course_sections=CourseSectionsSerializer().serialize(course_sections))



@users.route('/students_course_sections/<student_id>', methods=['GET'])
def students_course_sections(student_id):
    """ It returns just course_sections in progress """
    student = models.Users.query.filter_by(id=student_id, type=1).first()

    if not student:
        return jsonify(result='invalid student id')

    students_course_sections_list = student.course_sections
    current_course_sections = []

    for course_section_student in students_course_sections_list:
        if course_section_student.status == 1:
            current_course_sections.append(course_section_student.course_section)

    return jsonify(students_course_sections=CourseSectionsSerializer().serialize(current_course_sections))


@users.route('/token_register/<user_id>', methods=['POST'])
def token_register(user_id):
    post_message = request.get_json()['post_message']
    user = models.Users.query.get(user_id)

    if user:
        user.push_notification_token = post_message['push_notification_token']
        db.session.commit()
        user_serialized = serializer.UsersSerializer().serialize([user])
        return jsonify(user= user_serialized), 200

    return jsonify(result = 'invalid user id'), 404


@users.route('/update_user_image/<user_id>', methods=['POST'])
def update_user_image(user_id):
    user = models.Users.query.get(user_id)
    user_serialized = serializer.UsersSerializer().serialize([user])
    if not user:
        return jsonify(result='invalid user id'), 404
    if 'image_file' not in request.files:
        return jsonify(result='No file part'), 404

    file = request.files['image_file']

    if file.filename == '':
        return jsonify(result='No selected file'), 400
    if not file or not allowed_file(file.filename):
        return jsonify(result='File with invalid format'), 400

    filename = secure_filename(file.filename)
    if not user.save_image(file):
        return jsonify(user=user_serialized), 400

    db.session.commit()
    user_serialized = serializer.UsersSerializer().serialize([user])
    return jsonify(user=user_serialized), 200

def allowed_file(filename):
    return '.' in filename and (filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS or 'asset.JPG' in filename)
'''
