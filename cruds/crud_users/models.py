import datetime
from backend import db
import os
import settings
import requests
import random
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.Text())
    name = db.Column(db.String(250))
    birth_date = db.Column(db.Date())
    gender = db.Column(db.String(1))
    address = db.Column(db.String(250))
    push_notification_token = db.Column(db.Text(), nullable=True)
    type = db.Column(db.Integer, db.ForeignKey('user_type.id'))
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'), nullable=True)
    image_path = db.Column(db.Text(), nullable=True)
    

    def set_fields(self, fields):
        self.username = fields.get('username')
        self.email = fields.get('email')
        self.name = fields.get('name')
        self.gender = fields.get('gender')
        self.address = fields.get('address')
        self.birth_date = datetime.datetime.strptime(fields.get('birth_date'), "%m-%d-%Y").date() if fields.get('birth_date') else None
        self.program_id = fields.get('program_id')
        self.type = self.type if self.type else fields.get('type')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save_image(self, file):
        file_name, _format = str(file.filename).rsplit('.', 1)
        user_name, domain = str(self.email).split('@', maxsplit=1)

        if not _format in settings.ALLOWED_EXTENSIONS:
            _format = 'jpg'

        files = {'image_file': file}
        headers = {
            "enctype": "multipart/form-data"
        }

        r = requests.post('http://eliakimdjango.pythonanywhere.com/save_profile_image',
                          files={'file': (user_name + str(random.randint(1000, 10000)) + '.' + _format, file,
                          headers, {'Expires': '0'})},
                          data={'old_file_path': self.image_path})
        # r = requests.post('http://127.0.0.1:2000/save_profile_image',
        #                   files={'file': (self.username + str(random.randint(1000, 10000)) + '.' + _format, file,
        #                                   headers, {'Expires': '0'})},
        #                   data={'old_file_path': self.image_path})
        if r.status_code==200:
            self.image_path = r.json()['result']
            return True
