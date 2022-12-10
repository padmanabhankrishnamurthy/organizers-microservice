from flask import Flask, request, jsonify, render_template
from rds_utils import insert_into_table, update_table, delete_from_table

application = Flask(__name__)

ORGANIZER_DB_TABLES = {
    "contact_info": ["org_id", "org_name", "non_profit", "email", "phone"],
    "banking_info": ["org_id", "routing_number", "account_number", "bank_name"],
    "address": ["org_id", "st_and_apt", "city", "state", "zipcode", "country"],
}

@application.route("/", methods=["GET"])
def welcome():
    return "Hello World!"

@application.route("/signup", methods=["POST"])
def onboard_user():
    """
    request body is the request_data that goes into insert_int_table
    """
    request_data = request.get_json()
    insert_into_table(request_data)
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
    application.run()