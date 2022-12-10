import pymysql

# rds cred
RDS_HOST = "http://e61561.c4dwsoa8ic0w.us-east-1.rds.amazonaws.com/"
RDS_USERNAME = "admin"
RDS_PASSWORD = "dbpassword"


def get_db_cursor():
    db = pymysql.connect(host=RDS_HOST, user=RDS_USERNAME, password=RDS_PASSWORD)
    cursor = db.cursor()
    cursor.execute("""use organizer""")
    return cursor


def insert_into_table(table_name, data: list):
    cursor = get_db_cursor()
    sql_command = f'insert into {table_name} ({",".join(**data)})'
    cursor.execute(sql_command)
    print("Insertion successful")


def generate_where_params_string(where_params: dict):
    """
    where_params: {key: (condition, value)}
    """
    string = ""
    for key, value in where_params.items():
        operator, operand = value[0], value[1]

        if type(operand) == str:
            operand = f'"{operand}"'

        string += f"{key}{operator}{operand} and"

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
    cursor = get_db_cursor()
    where_params_string = "and".join(
        [f"{key}{value}" for key, value in where_params.items()]
    )
    sql_command = f"delete from {table_name} where {where_params_string}"
    cursor.execute(sql_command)
    print("Deletion successful")


def update_table(table_name, update_params: dict, where_params: dict):
    """
    param update_params: dictionary of update params formatted as {key:value}
    param where_params: dictionary of where params formatted as {key:(condition, value)}, see example in delete_from_table() docstring
    """
    cursor = get_db_cursor()

    update_params_string = generate_params_string(update_params=update_params)
    where_params_string = generate_params_string(where_params=where_params)
    sql_command = (
        f"update  {table_name} set {update_params_string} where {where_params_string}"
    )

    cursor.execute(sql_command)
    print("Update completed.")
