from flask_login import UserMixin
from rds_utils import read_all_fields_from_table, insert_into_table

USER_TABLE_FIELDS = ["id", "name", "email"]


class User(UserMixin):
    def __init__(self, id_, name, email):
        self.id = id_
        self.name = name
        self.email = email

    @staticmethod
    def get(user_id):
        user = read_all_fields_from_table(
            table_name="user", where_params={"id": user_id}
        )
        if not user:
            return None

        user = User(
            id_=user[0],
            name=user[1],
            email=user[2],
        )
        return user

    @staticmethod
    def create(id_, name, email):
        insert_into_table("user", data=[id_, name, email])
