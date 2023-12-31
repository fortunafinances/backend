import json
from urllib.request import urlopen

from authlib.oauth2.rfc7523 import JWTBearerTokenValidator
from authlib.jose.rfc7517.jwk import JsonWebKey
import sys

class Auth0JWTBearerTokenValidator(JWTBearerTokenValidator):
    def __init__(self, domain, audience):
        issuer = f"https://dev-wpc8kymxzmepqxl5.us.auth0.com/"
        jsonurl = urlopen(f"https://dev-wpc8kymxzmepqxl5.us.auth0.com/.well-known/jwks.json")
        public_key = JsonWebKey.import_key_set(
            json.loads(jsonurl.read())
        )
        super(Auth0JWTBearerTokenValidator, self).__init__(
            public_key
        )
        self.claims_options = {
            "exp": {"essential": True},
            "aud": {"essential": True, "value": audience},
            "iss": {"essential": True, "value": issuer},
        }
    def get_Token():
        token = JWTBearerTokenValidator.token_cls
        print("I GOT IT: " , token, file=sys.stdout)