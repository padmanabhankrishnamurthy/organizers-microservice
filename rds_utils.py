import pymysql

# rds cred
RDS_HOST = "nimbus-db.c4dwsoa8ic0w.us-east-1.rds.amazonaws.com"
RDS_USERNAME = "admin"
RDS_PASSWORD = "dbpassword"
RDS_PORT = 3306


def get_db_cursor():
    db = pymysql.connect(
        host=RDS_HOST, user=RDS_USERNAME, password=RDS_PASSWORD, port=RDS_PORT
    )
    cursor = db.cursor()
    cursor.execute("""use organizer""")
    return cursor, db


def read_all_fields_from_table(table_name, where_params: dict):
    cursor, db = get_db_cursor()

    where_params_string = generate_where_params_string(where_params=where_params)
    sql_command = f"select * from {table_name} where {where_params_string}"

    print(sql_command)
    cursor.execute(sql_command)

    result = cursor.fetchone()
    print(f"Result: {result}")
    return result


def insert_into_table(table_name, data: list):
    cursor, db = get_db_cursor()
    sql_command = (
        f'insert into {table_name} values ({",".join([str(item) for item in data])})'
    )
    print(sql_command)
    cursor.execute(sql_command)
    db.commit()
    print(f"Insertion into {table_name} successful\n")


def generate_where_params_string(where_params: dict):
    """
    where_params: {key: value}
    """
    string = ""
    for key, value in where_params.items():

        if type(value) == str:
            value = f'"{value}"'

        string += f"{key}={value} and"

    # trim the trailing and
    return string[: string.rfind(" and")]


def generate_params_string(params: dict):
    """
    params: {key:value}
    """
    string = ""
    for key, value in params.items():
        if type(value) == str:
            value = f'"{value}"'
        string += f"{value}, "

    # trim the trailing comma
    return string[: string.rfind(",")]


def delete_from_table(table_name, where_params: dict):
    """
    param data: dictionary of delete params formatted as {key:(condition, value)}
    NOTE: string values should be passed with quotes
    eg: for "delete from * where city='bangalore' and age>=30" the data dict would be
    {"city":("=","bangalore"), "age":(">=", 30)}
    """
    cursor, db = get_db_cursor()
    where_params_string = "and".join(
        [f"{key}{value}" for key, value in where_params.items()]
    )
    sql_command = f"delete from {table_name} where {where_params_string}"
    cursor.execute(sql_command)
    db.commit()
    print("Deletion successful\n")


def update_table(table_name, update_params: dict, where_params: dict):
    """
    param update_params: dictionary of update params formatted as {key:value}
    param where_params: dictionary of where params formatted as {key:(condition, value)}, see example in delete_from_table() docstring
    """
    cursor, db = get_db_cursor()

    update_params_string = generate_params_string(update_params=update_params)
    where_params_string = generate_params_string(where_params=where_params)
    sql_command = (
        f"update  {table_name} set {update_params_string} where {where_params_string}"
    )

    cursor.execute(sql_command)
    db.commit()
    print("Update completed\n")
