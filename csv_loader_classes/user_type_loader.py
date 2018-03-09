from csv_loader import CSVLoader


class UserTypeLoader(CSVLoader):

    def create_object(self, row):
        """ row[0] - id;
            row[1] - name;
        """
        user_type_class = self.import_relative_path('cruds.crud_user_type.models.UserType')

        user_type = self.session.query(user_type_class).get(row[0])

        if user_type:
            return

        obj = user_type_class()
        obj.name = row[1]

        return obj

    def file_name(self):
        return 'user_type.csv'
