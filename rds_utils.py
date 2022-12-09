import pymysql
from datetime import datetime

# rds cred
RDS_HOST = "http://e61561.c4dwsoa8ic0w.us-east-1.rds.amazonaws.com/"
RDS_USERNAME = "admin"
RDS_PASSWORD = "dbpassword"


def insert_into_table(table_name, data: list):
    cursor = get_db_cursor()
    sql_command = f'insert into {table_name} ({",".join(**data)})'
    cursor.execute(sql_command)
    print("Insertion successful")


def delete_from_table(table_name, delete_params: dict):
    """
    param data: dictionary of delete params formatted as {key:(condition, value)}
    NOTE: string values should be passed with quotes
    eg: for "delete from * where city='bangalore' and age>=30" the data dict would be
    {"city":("=","bangalore"), "age":(">=", 30)}
    """
    cursor = get_db_cursor()
    delete_params_string = "and".join(
        [f"{key}{value}" for key, value in delete_params.items()]
    )
    sql_command = f"delete from {table_name} where {delete_params_string}"
    cursor.execute(sql_command)
    print("Deletion successful")


def update_table(table_name, update_params: dict, where_params: dict):
    """
    param update_params: dictionary of update params formatted as {key:value}
    param where_params: dictionary of where params formatted as {key:<condition><value>}, see example in delete_from_table() docstring
    NOTE: again, string values should be passed with quotes eg: "where city="bangalore"" should be passed as {'city':'"bangalore"'}
    """
    cursor = get_db_cursor()
    update_params_string = ','.join([f"{key}={value}"])
    where_params_string = "and".join([f"{key}{value}" for key,value in where_params.items()])


def get_db_cursor():
    db = pymysql.connect(host=RDS_HOST, user=RDS_USERNAME, password=RDS_PASSWORD)
    cursor = db.cursor()
    cursor.execute("""use organizer""")
    return cursor


def db_insert_all_requests(original_video_url, source_language, target_language, email):
    cursor = get_db_cursor()
    sql = """insert into all_requests (original_video_url, source_language, target_language, email, time)
    values ('%s','%s','%s','%s','%s')""" % (
        original_video_url,
        source_language,
        target_language,
        email,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    cursor.execute(sql)
    cursor.connection.commit()


def db_insert_waitlist(name, email):
    cursor = get_db_cursor()
    sql = """insert into waitlist (name, email, time)
    values ('%s','%s','%s')""" % (
        name,
        email,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    cursor.execute(sql)
    cursor.connection.commit()


def db_insert_translate_requests(
    email,
    source_language,
    target_language,
    original_video_url,
    platform,
    video_id,
    translated_video_url="",
    status="processing",
):
    cursor = get_db_cursor()
    sql = """insert into translate_requests (email,source_language,target_language,original_video_url,platform,video_id, translated_video_url, status, time)
    values ('%s','%s','%s','%s','%s','%s','%s','%s','%s')""" % (
        email,
        source_language,
        target_language,
        original_video_url,
        platform,
        video_id,
        translated_video_url,
        status,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    cursor.execute(sql)
    cursor.connection.commit()


def db_select_translate_requests(
    platform, video_id, source_language, target_language, email=None
):
    cursor = get_db_cursor()
    if email:
        sql = f"""select * from translate_requests
        where platform='%s' and video_id='%s' and source_language='%s' and target_language='%s' and email='%s' """ % (
            platform,
            video_id,
            source_language,
            target_language,
            email,
        )
    else:
        sql = f"""select * from translate_requests
        where platform='%s' and video_id='%s' and source_language='%s' and target_language='%s' """ % (
            platform,
            video_id,
            source_language,
            target_language,
        )
    cursor.execute(sql)
    return cursor.fetchall()


def db_update_translate_requests_completed(
    platform, video_id, source_language, target_language, translated_video_url
):
    cursor = get_db_cursor()
    sql = f"""update translate_requests
    set status='completed', translated_video_url='%s'
    where platform='%s' and video_id='%s' and source_language='%s' and target_language='%s' """ % (
        translated_video_url,
        platform,
        video_id,
        source_language,
        target_language,
    )
    cursor.execute(sql)
    cursor.connection.commit()
