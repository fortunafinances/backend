import jwt
from flask import Blueprint, jsonify, request
from functools import wraps
import sys
from flask_cors import CORS

api_blueprint = Blueprint('api', __name__)

def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        print("AUTH HEADER.... ", auth_header, " ", file=sys.stdout)
        if not auth_header:
            return {'message': 'Authorization header is missinggg'}, 401

        token = auth_header.split(' ')[1]
        print("\nTOKEN.... ", token, " ", file=sys.stdout)
        # TODO: validate the token using Auth0's API
        # if the token is valid, extract the user information and pass it to the wrapped function
        
        
        try:
          print("\nSTARTING DECODING ACCESS TOKEN...", file=sys.stdout)
          # decode the token using the secret key used to sign it
          decoded_token = jwt.decode(token, 'my_secret_key', algorithms=['HS256'])
          # extract the user information from the decoded token
          user_info = {
              'name': decoded_token['name'],
              'email': decoded_token['email']
          }
          return {'user_info': user_info}, 200
        except jwt.exceptions.InvalidTokenError:
          return {'message': 'Invalid token'}, 401
    return wrapper

@api_blueprint.route('/api/users', methods=['GET'])
@authenticate
def get_user_info(user_info):
    # use the user_info to return the user's information
    return {'message': f'Hello {user_info["name"]}'}

