from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from ariadne import graphql_sync, make_executable_schema, gql, load_schema_from_path
from ariadne.explorer import ExplorerGraphiQL

from model import query, mutation
import sys
sys.path.insert(0, '../database')

from stock import Stock




"""
    This is the server file which handles the GraphQL route. The route we
    will be using is /graphql

    This file is run using the "py server.py" command (or "python server.py")
    in your terminal.
"""

EXPLORER_HTML = ExplorerGraphiQL().html(None)

type_defs = gql(load_schema_from_path("schema.graphql"))
schema = make_executable_schema(type_defs, query, mutation)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../database/database.db'
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

@app.route('/')
def hello_world():
    # test insertion, works in here, no clue about elsewhere
    stock1 = Stock(
        ticker = "TSLA", 
        currPrice = 20523, 
        highPrice = 24543, 
        lowPrice = 19234, 
        openPrice = 20326, 
        prevClosePrice = 21032
        )
    db.session.add(stock1)
    db.session.commit()
    return 'Hello, World!'


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return EXPLORER_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()

    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == '__main__':
    app.run(debug=True)  # debug=True allows the server to restart itself
                         # to provide constant updates to the developer
    