from csv_loader import CSVLoader
from cruds.crud_course_sections.models import CourseSections
import datetime

class SectionTimesLoader(CSVLoader):

    def create_object(self, row):
        """ row[0] - id;
            row[1] - course section code
            row[2] - course section period;
            row[3] - week_day;
            row[4] - section_time_start_time;
            row[5] - section_time_finish_time;
        """
        section_times_class = self.import_relative_path('cruds.crud_section_times.models.SectionTimes')

        section_times = self.session.query(section_times_class).get(row[0])

        if section_times:
            return

        obj = section_times_class()
        obj.course_section_id = self.session.query(CourseSections).filter(CourseSections.code==row[1], CourseSections.course_section_period==row[2]).first().id
        obj.week_day = row[3]
        obj.section_time_start_time = datetime.datetime.strptime(row[4], "%H:%M:%S").time()
        obj.section_time_finish_time = datetime.datetime.strptime(row[5], "%H:%M:%S").time()

        return obj

    def file_name(self):
        return 'section_times.csv'
