from csv_loader import CSVLoader
import datetime


class CourseSectionStudentsStatusLoader(CSVLoader):

    def create_object(self, row):
        """ row[0] - id;
            row[1] - description;
        """
        course_section_students_status_class = self.import_relative_path('cruds.crud_course_section_students_status.models.CourseSectionStudentsStatus')

        course_section_students_status = self.session.query(course_section_students_status_class).get(row[0])

        if course_section_students_status:
            return

        obj = course_section_students_status_class()
        obj.description = row[1]

        return obj

    def file_name(self):
        return 'course_section_students_status.csv'
