from csv_loader import CSVLoader
from cruds.crud_user_type.models import UserType
from cruds.crud_program.models import Program
import datetime
from werkzeug.security import generate_password_hash


class UsersLoader(CSVLoader):

    def create_object(self, row):
        """ row[0] - id;
            row[1] - username;
            row[2] - email;
            row[3] - password;
            row[4] - name;
            row[5] - birth_date;
            row[6] - gender;
            row[7] - address;
            row[8] - type;
            row[9] - program_id;
        """
        users_class = self.import_relative_path('cruds.crud_users.models.Users')

        user = self.session.query(users_class).filter_by(email=row[2]).first()

        if user:
            return

        obj = users_class()
        obj.username = row[1]
        obj.email = row[2]
        obj.password = generate_password_hash(row[3])
        obj.name = row[4]
        obj.birth_date = datetime.datetime.strptime(row[5], "%d-%m-%Y").date()
        obj.gender = row[6]
        obj.address = row[7]
        obj.type = self.session.query(UserType).filter(UserType.name==row[8]).first().id
        obj.program_id = self.session.query(Program).filter(Program.abbreviation==row[9]).first().id if self.session.query(Program).filter(Program.abbreviation==row[9]).first() else None

        return obj

    def file_name(self):
        return 'users.csv'
