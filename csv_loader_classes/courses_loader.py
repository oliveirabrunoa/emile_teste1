from csv_loader import CSVLoader
from cruds.crud_program.models import Program
from cruds.crud_course_type.models import CourseType


class CoursesLoader(CSVLoader):

    def create_object(self, row):
        """ row[0] - id;
            row[1] - code;
            row[2] - name;
            row[3] - credits;
            row[4] - hours;
            row[5] - program_section;
            row[6] - course_type_description;
            row[7] - program_abbreviation; """

        course_class = self.import_relative_path('cruds.crud_courses.models.Courses')

        course = self.session.query(course_class).get(row[0])

        if course:
            return

        obj = course_class()
        obj.code = row[1]
        obj.name = row[2]
        obj.credits = row[3]
        obj.hours = row[4]
        obj.program_section = row[5]
        obj.course_type_id = self.session.query(CourseType).filter(CourseType.description==row[6]).first().id
        obj.program_id = self.session.query(Program).filter(Program.abbreviation==row[7]).first().id

        return obj

    def file_name(self):
        return 'courses.csv'
