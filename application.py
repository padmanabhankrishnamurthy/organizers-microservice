from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from rds_utils import insert_into_table, update_table, delete_from_table

application = Flask(__name__)
CORS(application)

ORGANIZER_DB_TABLES = {
    "contact_info": ["org_id", "org_name", "non_profit", "email", "phone"],
    "banking_info": ["org_id", "routing_number", "account_number", "bank_name"],
    "address": ["org_id", "st_and_apt", "city", "state", "zipcode", "country"],
}

MOST_RECENT_ORGANIZER_ID = 0


@application.route("/", methods=["GET"])
def welcome():
    return "Hello World!"


@application.route("/signup_page", methods=["GET"])
def signup_page():
    return render_template("organizer_signup.html")


@application.route("/signup", methods=["POST"])
def onboard_user():
    """
    request body is the request_data that goes into insert_int_table
    """
    # update global org id, TODO: read most recent org id from an organizers table
    global MOST_RECENT_ORGANIZER_ID
    MOST_RECENT_ORGANIZER_ID += 1

    request_data = request.get_json()
    request_data["org_id"] = MOST_RECENT_ORGANIZER_ID

    # insert into all tables
    for table_name, column_names in ORGANIZER_DB_TABLES.items():
        insert_into_table(
            table_name=table_name,
            data=[request_data[column_name] for column_name in column_names],
        )

    return jsonify({"status": "signup insertion completed"})


@application.route("/update", methods=["POST"])
def update_account():
    """
    request body is {"update_params":{update_params}, "where_params":{where_params}}
    """
    request_data = request.get_json()
    update_table(request_data["update_params"], request_data["where_params"])
    return jsonify({"status": "account update completed"})


@application.route("/delete_account", methods=["POST"])
def delete_account():
    """
    request body is where_params that goes straight into delete_from_table()
    """
    request_data = request.get_json()

    for table_name in ORGANIZER_DB_TABLES.keys():
        delete_from_table(table_name=table_name, where_params=request_data)

    return jsonify({"status": "account deleted"})


if __name__ == "__main__":
    application.run(debug=True)
