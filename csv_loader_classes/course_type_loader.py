from csv_loader import CSVLoader
import datetime


class CourseTypeLoader(CSVLoader):

    def create_object(self, row):
        """ row[0] - id;
            row[1] - description;
        """
        course_type_class = self.import_relative_path('cruds.crud_course_type.models.CourseType')

        course_type = self.session.query(course_type_class).get(row[0])

        if course_type:
            return

        obj = course_type_class()
        obj.description = row[1]

        return obj

    def file_name(self):
        return 'course_type.csv'
