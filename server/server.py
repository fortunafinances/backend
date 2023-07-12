from flask import Flask, request, jsonify, make_response
from ariadne import graphql_sync, make_executable_schema, gql, load_schema_from_path
from ariadne.explorer import ExplorerGraphiQL
from flask_cors import CORS, cross_origin
from model import query, mutation
from apiRequests import get_stock_quote



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


@app.route('/')
@cross_origin()
def hello_world():
    return 'Hello, World!'


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

if __name__ == '__main__':
    app.run(debug=True)  # debug=True allows the server to restart itself
                         # to provide constant updates to the developer
# defining GET request for a quote
@app.route('/get_quote/<symbol>', methods=["GET"])
def get_quote(symbol):
    return get_stock_quote(symbol)

if __name__ == '__main__':
    app.run(debug=True)

    
