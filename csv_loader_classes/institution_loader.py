from csv_loader import CSVLoader


class InstitutionLoader(CSVLoader):

    def create_object(self, row):
        """ row[0] - id;
            row[1] - name;
            row[2] - abbreviation;
            row[3] - cnpj;
            row[4] - address;
            row[5] - current_program_section
        """
        institution_class = self.import_relative_path('cruds.crud_institution.models.Institution')

        institution = self.session.query(institution_class).get(row[0])

        if institution:
            return

        obj = institution_class()
        obj.name = row[1]
        obj.abbreviation = row[2]
        obj.cnpj = row[3]
        obj.address = row[4]
        obj.current_program_section = row[5]

        return obj

    def file_name(self):
        return 'institution.csv'
