from csv_loader import CSVLoader
from cruds.crud_users.models import Users
from cruds.crud_course_sections.models import CourseSections
from cruds.crud_course_section_students_status.models import CourseSectionStudentsStatus


class CourseSectionsStudentsLoader(CSVLoader):

    def create_object(self, row):
        """ row[0] - id;
            row[1] - course_section_code;
            row[2] - course_section_course_section_period;
            row[3] - student_username;
            row[4] - course_section_students_status_description;
            row[5] - grade; """

        course_sections_students_class = self.import_relative_path('cruds.crud_course_section_students.models.CourseSectionStudents')

        course_section_student = self.session.query(course_sections_students_class).get(row[0])

        if course_section_student:
            return

        obj = course_sections_students_class()
        obj.course_section_id = self.session.query(CourseSections).filter(CourseSections.code==row[1],
                                                                          CourseSections.course_section_period==row[2]).first().id
        obj.user_id = self.session.query(Users).filter(Users.username==row[3]).first().id
        obj.status = self.session.query(CourseSectionStudentsStatus).filter(CourseSectionStudentsStatus.description==row[4]).first().id
        obj.grade = row[5]

        return obj

    def file_name(self):
        return 'course_section_students.csv'
