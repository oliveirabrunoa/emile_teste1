from csv_loader import CSVLoader
from cruds.crud_user_type_destinations.models import UserTypeDestinations
from cruds.crud_user_type.models import UserType


class UserTypeDestinationsUserTypeLoader(CSVLoader):

    def create_object(self, row):
        """ row[0] - id;
            row[1] - user_type_id;
            row[2] - user_type_destination_id;
        """
        user_type_destinations_user_type_class = self.import_relative_path('cruds.crud_user_type_destinations_user_type.models.UserTypeDestinationsUserType')

        user_type_destination_user_type = self.session.query(user_type_destinations_user_type_class).get(row[0])

        if user_type_destination_user_type:
            return

        obj = user_type_destinations_user_type_class()
        obj.user_type_id = self.session.query(UserType).filter(UserType.name==row[1]).first().id
        obj.user_type_destination_id = self.session.query(UserTypeDestinations).filter(UserTypeDestinations.name==row[2]).first().id

        return obj

    def file_name(self):
        return 'user_type_destinations_user_type.csv'
