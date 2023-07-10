from flask import Flask, request, jsonify
from ariadne import graphql_sync, make_executable_schema, gql, load_schema_from_path
from ariadne.explorer import ExplorerGraphiQL

from model import query, mutation
from model2 import query as query2, mutation as mutation2


"""
    This is the server file which handles the GraphQL routes such as 
    /graphql or /newOrder
    Information for each route will be held in separte files titled model.py
    for /graphql or model2.py for /newOrder

    This file is run using the "py server.py" command (or "python server.py")
    in your terminal.
"""


EXPLORER_HTML = ExplorerGraphiQL().html(None)

type_defs = gql(load_schema_from_path("schema.graphql"))
schema = make_executable_schema(type_defs, query, mutation)

type_defs2 = gql(load_schema_from_path("schema2.graphql"))
schema2 = make_executable_schema(type_defs2, query2, mutation2)

app = Flask(__name__)


@app.route('/')
def hello_world():
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


@app.route("/placeOrder", methods=["GET"])
def newfunc():
    return EXPLORER_HTML, 200

@app.route("/placeOrder", methods=["POST"])
def newfunc_server():
    data = request.get_json()

    success, result = graphql_sync(
        schema2,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code



if __name__ == '__main__':
    app.run(debug=True)