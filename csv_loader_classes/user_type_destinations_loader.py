from csv_loader import CSVLoader


class UserTypeDestinationsLoader(CSVLoader):

    def create_object(self, row):
        """ row[0] - id;
            row[1] - name;
            row[2] - param_values_service;
            row[3] - users_query;
            row[4] - group;
            row[5] - group_module;
        """
        user_type_destinations_class = self.import_relative_path('cruds.crud_user_type_destinations.models.UserTypeDestinations')

        user_type_destination = self.session.query(user_type_destinations_class).get(row[0])

        if user_type_destination:
            return

        obj = user_type_destinations_class()
        obj.name = row[1]
        obj.param_values_service = row[2]
        obj.users_query = row[3]
        obj.group = row[4]
        obj.group_module = row[5]

        return obj

    def file_name(self):
        return 'user_type_destinations.csv'
