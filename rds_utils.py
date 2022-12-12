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


def generate_params_string(params: dict, conjunction="and"):
    """
    params: {key: value}
    """
    string = ""
    for key, value in params.items():

        if type(value) == str:
            value = f'"{value}"'

        string += f"{key}={value} {conjunction} "

    # trim the trailing and
    return string[: string.rfind(f" {conjunction}")]


def get_current_max_org_id():
    cursor, db = get_db_cursor()

    sql_command = "select max(cast(org_id as unsigned)) from contact_info"
    print(sql_command)
    cursor.execute(sql_command)

    result = cursor.fetchone()[0]
    print(f"Max org_id: {result}")
    if result:
        return result
    else:
        return 0


def read_all_fields_from_table(table_name, where_params: dict):
    cursor, db = get_db_cursor()

    where_params_string = generate_params_string(params=where_params)
    sql_command = f"select * from {table_name} where {where_params_string}"

    print(sql_command)
    cursor.execute(sql_command)

    result = cursor.fetchone()
    print(f"Result: {result}")
    return result


def insert_into_table(table_name, data: list):
    cursor, db = get_db_cursor()

    items_string = ""
    for element in data:
        if type(element) == str:
            items_string += f'"{element}", '
        else:
            items_string += f"{element}, "
    items_string = items_string[: items_string.rfind(", ")]
    sql_command = f"insert into {table_name} values ({items_string})"
    print(sql_command)

    cursor.execute(sql_command)
    db.commit()
    print(f"Insertion into {table_name} successful\n")


def delete_from_table(table_name, where_params: dict):
    """
    param data: dictionary of delete params formatted as {key:(condition, value)}
    NOTE: string values should be passed with quotes
    eg: for "delete from * where city='bangalore' and age>=30" the data dict would be
    {"city":("=","bangalore"), "age":(">=", 30)}
    """
    cursor, db = get_db_cursor()
    where_params_string = generate_params_string(params=where_params)

    sql_command = f"delete from {table_name} where {where_params_string}"
    print(sql_command)
    cursor.execute(sql_command)
    db.commit()

    print("Deletion successful\n")


def update_table(table_name, update_params: dict, where_params: dict):
    """
    param update_params: dictionary of update params formatted as {key:value}
    param where_params: dictionary of where params formatted as {key:value}
    """
    cursor, db = get_db_cursor()

    update_params_string = generate_params_string(params=update_params, conjunction=",")
    where_params_string = generate_params_string(params=where_params)
    sql_command = (
        f"update  {table_name} set {update_params_string} where {where_params_string}"
    )
    print(sql_command)

    cursor.execute(sql_command)
    db.commit()
    print("Update completed\n")
