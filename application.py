import os
import json
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests
from flask_cors import CORS
from rds_utils import (
    insert_into_table,
    update_table,
    delete_from_table,
    read_all_fields_from_table,
    get_current_max_org_id,
)
from utils import get_google_ouath_keys
from user import User

application = Flask(__name__)
application.secret_key = os.urandom(24)
CORS(application)

# google oauth config 
GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET = get_google_ouath_keys()
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
client = WebApplicationClient(GOOGLE_CLIENT_ID)
login_manager = LoginManager()
login_manager.init_app(application)

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

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@application.route("/", methods=["GET"])
def welcome():
    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email, current_user.profile_pic
            )
        )
    else:
        return '<a class="button" href="/login">Google Login</a>'

@application.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@application.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))


@application.route("/login_page", methods=["GET"])
def login_page():
    return render_template("login_page.html")


@application.route("/onboard_page", methods=["GET"])
def onboard_page():
    return render_template("organizer_onboard.html")


@application.route("/display_events_page", methods=["GET"])
def display_events():
    return render_template("display_events.html")


@application.route("/account_page/<org_id>", methods=["GET"])
def account_page(org_id):
    account_info = {}
    where_params = {"org_id": org_id}

    for table_name, columns in ORGANIZER_DB_TABLES.items():
        row = read_all_fields_from_table(
            table_name=table_name, where_params=where_params
        )
        info = zip(columns, row)
        account_info.update(info)

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
