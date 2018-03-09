from csv_loader import CSVLoader
from cruds.crud_institution.models import Institution


class ProgramLoader(CSVLoader):

    def create_object(self, row):
        """ row[0] - id;
            row[1] - name;
            row[2] - abbreviation;
            row[3] - total_hours;
            row[4] - total_credits;
            row[5] - institution_cnpj
            row[6] - coordinator_id
        """
        program_class = self.import_relative_path('cruds.crud_program.models.Program')

        program = self.session.query(program_class).get(row[0])

        if program:
            return

        obj = program_class()
        obj.name = row[1]
        obj.abbreviation = row[2]
        obj.total_hours = row[3]
        obj.total_credits = row[4]
        obj.institution_id = self.session.query(Institution).filter(Institution.cnpj==row[5]).first().id
        obj.coordinator_id = row[6] if row[6] else None

        return obj

    def file_name(self):
        return 'program.csv'
