from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from rds_utils import (
    insert_into_table,
    update_table,
    delete_from_table,
    read_all_fields_from_table,
    get_current_max_org_id,
)

application = Flask(__name__)
CORS(application)

ORGANIZER_DB_TABLES = {
    "contact_info": [
        "org_id",
        "org_name",
        "non_profit",
        "email",
        "phone",
    ],
    "banking_info": [
        "org_id",
        "routing_number",
        "account_number",
        "bank_name",
    ],
    "address": [
        "org_id",
        "st_and_apt",
        "city",
        "state",
        "zipcode",
        "country",
    ],
    #     "events": [
    #         "event_id",
    #         "org_id",
    #         "date",
    #         "start_time",
    #         "end_time",
    #         "description",
    #         "event_category",
    #         "capacity",
    #         "event_name",
    #         "image",
    #     ],
}

# inverse of ORGANIZER_DB_TABLES
COLUMN_TABLE_MAPPING = {}
for table_name, columns in ORGANIZER_DB_TABLES.items():
    for column in columns:
        COLUMN_TABLE_MAPPING[column] = table_name


@application.route("/", methods=["GET"])
def welcome():
    return "Hello World!"


@application.route("/login_page", methods=["GET"])
def login_page():
    return render_template("login_page.html")


@application.route("/onboard_page", methods=["GET"])
def onboard_page():
    return render_template("organizer_onboard.html")


@application.route("/display_events_page", methods=["GET"])
def display_events():
    return render_template("display_events.html")


def get_account_info(org_id):
    account_info = {}
    where_params = {"org_id": org_id}

    for table_name, columns in ORGANIZER_DB_TABLES.items():
        row = read_all_fields_from_table(
            table_name=table_name, where_params=where_params
        )
        info = zip(columns, row)
        account_info.update(info)

    return account_info


@application.route("/get_account_info/<org_id>", methods=["POST"])
def account_page(org_id):
    account_info = get_account_info(org_id)
    print(f"Account Info: {account_info}")
    return jsonify(account_info)


@application.route("/account_page/<org_id>", methods=["GET"])
def account_page(org_id):
    account_info = get_account_info(org_id)
    print(f"Account Info: {account_info}")
    return render_template("account_page.html", account_info=account_info)


@application.route("/edit_page/<org_id>", methods=["GET"])
def edit_page(org_id):
    account_info = {}
    where_params = {"org_id": org_id}

    for table_name, columns in ORGANIZER_DB_TABLES.items():
        row = read_all_fields_from_table(
            table_name=table_name, where_params=where_params
        )
        info = zip(columns, row)
        account_info.update(info)

    print(f"Account Info: {account_info}")
    return render_template("edit_info.html", account_info=account_info)


@application.route("/add_event_page/<org_id>", methods=["GET"])
def add_event_page(org_id):
    account_info = {}
    where_params = {"org_id": org_id}
    return render_template("add_event.html", account_info=account_info)


@application.route("/onboard_api", methods=["POST"])
def onboard_user():
    """
    request body is the request_data that goes into insert_int_table
    """

    request_data = request.get_json()

    current_max_org_id = get_current_max_org_id()
    request_data["org_id"] = current_max_org_id + 1

    # insert into all tables
    for table_name, column_names in ORGANIZER_DB_TABLES.items():
        insert_into_table(
            table_name=table_name,
            data=[request_data[column_name] for column_name in column_names],
        )

    return jsonify(
        {"status": "onboard insertion completed", "org_id": request_data["org_id"]}
    )


@application.route("/edit_api", methods=["POST"])
def update_account():
    """
    request body is {"update_params":{update_params}, "where_params":{"org_id":org_id}}
    """
    request_data = request.get_json()
    print(f"Request: {request_data}")

    update_params = request_data["update_params"]

    # incoming update_params is {column:value}, but update_table() needs table_name
    # so create update_tables where update_tables[table_name] = {update_params of columns beloning to table_name}
    update_tables = {table_name: {} for table_name in ORGANIZER_DB_TABLES}
    for update_column, value in update_params.items():
        update_column_table = COLUMN_TABLE_MAPPING[
            update_column
        ]  # table to which update_column belongs
        update_tables[update_column_table][update_column] = value

    print(f"update_tables: {update_tables}")

    for table_name, update_params in update_tables.items():
        if len(update_params.keys()) == 0:
            continue
        update_table(
            table_name=table_name,
            update_params=update_params,
            where_params=request_data["where_params"],
        )

    return jsonify({"status": "account update completed"})


@application.route("/add_event_api", methods=["POST"])
def add_event():
    request_data = request.get_json()
    insert_into_table(table_name="events", data=request_data)
    return jsonify({"status": "event created"})


@application.route("/delete_account_api", methods=["POST"])
def delete_account():
    """
    request body is where_params that goes straight into delete_from_table()
    in this case, where params should be {"org_id": org_id_to_delete}
    """
    request_data = request.get_json()

    # reverse the order of table deletion so that foreign key referencers are deleted first, and the og key deleted last
    for table_name in list(ORGANIZER_DB_TABLES.keys())[::-1]:
        delete_from_table(table_name=table_name, where_params=request_data)

    return jsonify({"status": "account deleted"})


if __name__ == "__main__":
    application.run(debug=True)
