from flask import Flask, request, jsonify, make_response
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from ariadne import graphql_sync, make_executable_schema, gql, load_schema_from_path
from ariadne.explorer import ExplorerGraphiQL
from apscheduler.schedulers.background import BackgroundScheduler
import time
import logging
import sys

#from fsi-23-bos-back-end.database.inserters import fillStocks
from flask_cors import CORS, cross_origin
from usersApi import api_blueprint

# Database file imports
sys.path.insert(0, '../database')
import inserters
import getters
from tables import db

sys.path.insert(0, '../mockData')
import mockDb
from stockConfig import fillStocks
from constants import SP_500

sys.path.insert(0, './graphQL')
from mutations import mutation
from queries import query

sys.path.insert(0, './scheduler')
from schedule import scheduler, updateStockHistory, updateSP500

sys.path.insert(0, './stockAPI')
from dataProcessing import handle_metadata
from apiRequests import get_stock_metadata, get_stock_quote

# Auth0 imports
from authlib.integrations.flask_oauth2 import ResourceProtector
from authlib.integrations.flask_client import OAuth
from authlib.oauth2 import OAuth2Error

sys.path.insert(0, '../authentication')
from validator import Auth0JWTBearerTokenValidator

# Auth0 imports
from authlib.integrations.flask_oauth2 import ResourceProtector
from authlib.integrations.flask_client import OAuth
from authlib.oauth2 import OAuth2Error

sys.path.insert(0, '../authentication')
from validator import Auth0JWTBearerTokenValidator

require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    "dev-wpc8kymxzmepqxl5.us.auth0.com",
    "https://dev-wpc8kymxzmepqxl5.us.auth0.com/api/v2/"
)
require_auth.register_token_validator(validator)

"""
    This is the server file which handles the GraphQL route. The route we
    will be using is /graphql

    This file is run using the "py server.py" command (or "python server.py")
    in your terminal.
"""

EXPLORER_HTML = ExplorerGraphiQL().html(None)

type_defs = gql(load_schema_from_path('./graphQL/schema.graphql'))
schema = make_executable_schema(type_defs, query, mutation)
app = Flask(__name__)
CORS(app)

# Database initialisation 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../database/database.db'
db.init_app(app)

app.config['SCHEDULER_TIMEZONE'] = 'America/New_York'
scheduler.init_app(app)
scheduler.start()

# Create an instance of OAuth
oauth = OAuth(app)

@app.route('/')
@cross_origin()
def hello_world():
    return 'Hello, World!'

# Functionality testing route.
# Allows for different aspects of the database to be tested
# You may need to uncomment/comment certain functions in
# get functions return the query data and insert functions 
# do not.
@app.route("/test")
def test():
    return str(getters.getStockHistory("HD"))
    
@app.route("/createMockDb")
def createMockDb():
    fillStocks()
    mockDb.initUsers()
    mockDb.initAccs()
    mockDb.initBuyMarket()
    mockDb.initSellMarket()
    mockDb.initTransferIn()
    mockDb.initTransferOut()
    mockDb.initTransferBetween()
    return "MockDb created"

""" ----------------- Auth testing ----------------- """
# auth test for protected route
@app.route("/api/private")
@require_auth(None)
def private():
    """A valid access token is required."""
    response = (
        "Hello from a private endpoint! You need to be"
        " authenticated to see this."
    )
    
    return jsonify(message=response)

data_list = []

@app.route('/add_user', methods=['POST'])
def add_data():
    data = request.get_json()
    data_list.append(data)
    # Process the data as needed
    # Example: Save the data to a database
    # Return a response
    return jsonify({'message': 'User received successfully'})

@app.route('/add_user', methods=['GET'])
def get_users():
    return jsonify(data_list)

""" ---------------- END AUTH TEST ----------------- """

# @app.route('/user')
# @require_oauth(['profile'])
# def user_profile():
#     user = User.query.get(current_token.user_id)
#     return jsonify(user.to_dict())

""" End of auth testing """

@app.route("/graphql", methods=["GET"])
@cross_origin()
def graphql_playground():
    return EXPLORER_HTML, 200


@app.route("/graphql", methods=["POST", "OPTIONS"])
@cross_origin()
def graphql_server():
    if request.method == "OPTIONS":   # CORS sends an options request from the frontend before a POST
        return _build_cors_preflight_response()
    elif request.method == "POST":
        data = request.get_json()

        success, result = graphql_sync(
            schema,
            data,
            context_value=request,
            debug=app.debug
        )

        response = jsonify(result)
        status_code = 200 if success else 400
        return response
    else:
        raise RuntimeError("Can not handle method {}".format(request.method))

"""
This is a helper method for the POST requests. It gives access control to the browser
to solve access for CORS.
"""
def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

# defining GET request for a quote
@app.route('/get_quote/<symbol>', methods=["GET"])
def get_quote(symbol):
    data = get_stock_quote(symbol)
    print(type(data))
    return data

# @app.route('/get_list/<exchange>', methods=["GET"])
# def get_list(exchange):
#     data = get_stock_list(exchange)
#     handled = handle_stock_list(data)
#     print(handled)
#     return data

@app.route('/get_meta/<symbol>', methods=['GET'])
def get_meta(symbol):
    data = get_stock_metadata(symbol)
    print(type(data))
    print(handle_metadata(data))
    return data


#This endpoint can be used to initialize the Stock table and update prices
@app.route('/testStocks')
def testStocks():
    inserters.fillStocks()
    return "The stock list has been updated"

"""
Auth
"""
app.register_blueprint(api_blueprint)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # schedule_jobs()
    app.run(use_reloader = False)  # debug=True allows the server to restart itself
                         # to provide constant updates to the developer