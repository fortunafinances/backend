from flask import Blueprint, current_app
from authlib.integrations.flask_client import OAuth

from config import config

auth_bp = Blueprint('auth', __name__)

auth0_config = config['AUTH0']
oauth = OAuth(current_app)

domain = auth0_config["DOMAIN"]
client_id = auth0_config["CLIENT_ID"]
client_secret = auth0_config["CLIENT_SECRET"]

# set up authlib with server detail
oauth.register(
    "auth0",
    client_id=client_id,
    client_secret=client_secret,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{domain}/.well-known/openid-configuration'
)