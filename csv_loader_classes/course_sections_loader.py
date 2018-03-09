from csv_loader import CSVLoader
from cruds.crud_users.models import Users
from cruds.crud_courses.models import Courses


class CourseSectionsLoader(CSVLoader):

    def create_object(self, row):
        """ row[0] - id;
            row[1] - code;
            row[2] - name;
            row[3] - course_code;
            row[4] - teacher_username;
            row[5] - course_section_period;"""

        course_sections_class = self.import_relative_path('cruds.crud_course_sections.models.CourseSections')

        course_section = self.session.query(course_sections_class).get(row[0])

        if course_section:
            return

        obj = course_sections_class()
        obj.code = row[1]
        obj.name = row[2]
        obj.course_id = self.session.query(Courses).filter(Courses.code==row[3]).first().id
        obj.teacher_id = self.session.query(Users).filter(Users.username==row[4]).first().id
        obj.course_section_period = row[5]

        return obj

    def file_name(self):
        return 'course_sections.csv'
