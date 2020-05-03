import json
from configparser import ConfigParser

from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

from src.utils.configs import get_auth0_variables

config_vars = get_auth0_variables()
AUTH0_DOMAIN = config_vars['auth0_domain']
ALGORITHMS = config_vars['algorithms']
API_AUDIENCE = config_vars['api_audience']


class AuthError(Exception):
    """
        A standardized way to communicate auth failure modes
    """

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """
        it attempts to get the header from the request
            it raises an AuthError if no header is present
        it attempts to split bearer and the token
            it raises an AuthError if the header is malformed

        :return: token
    """
    error = {
        'code': '',
        'description': ''
    }
    authorization = request.headers.get('Authorization', None)

    if not authorization:
        error['code'] = 'authorization_header_missing'
        error['description'] = 'Authorization header is expected.'
        raise AuthError(error, 401)

    parts = authorization.split()

    if parts[0].lower() != 'bearer':

        # parts[0] expected: bearer
        error['code'] = 'invalid_header'
        error['description'] = 'Authorization header must start with "Bearer".'
        raise AuthError(error, 401)

    elif len(parts) == 1:

        # parts[1] expected: token
        error['code'] = 'invalid_header'
        error['description'] = 'Token not found.'
        raise AuthError(error, 401)

    elif len(parts) > 2:

        # len(parts) expected: 2
        error['code'] = 'invalid_header'
        error['description'] = 'Authorization header must be bearer token.'
        raise AuthError(error, 401)

    token = parts[1]

    return token


'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''


def check_permissions(permission, payload):
    raise Exception('Not Implemented')


# !!NOTE urlopen has a common certificate error described here:
# https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
def verify_decode_jwt(token):
    """
        it is an Auth0 token with key id (kid)
        verifies the token using Auth0 /.well-known/jwks.json
        decodes the payload from the token
        validates the claims
        return the decoded payload

        :param token: a json web token (string)
        :return: payload
    """
    error = {
        'code': '',
        'description': ''
    }

    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    if 'kid' not in unverified_header:
        # kid is expected
        error['code'] = 'invalid_header'
        error['description'] = 'Authorization malformed.'
        raise AuthError(error, 401)

    # key used to sign the token is expected
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            # success
            return payload

        except jwt.ExpiredSignatureError:

            # expired token
            error['code'] = 'token_expired'
            error['description'] = 'Token expired.'
            raise AuthError(error, 401)

        except jwt.JWTClaimsError:

            # contents of the token is different than expected
            error['code'] = 'invalid_claims'
            error['description'] = 'Incorrect claims. Please, check the audience and issuer.'
            raise AuthError(error, 401)

        except Exception:

            # unexpected errors
            error['code'] = 'invalid_header'
            error['description'] = 'Unable to parse authentication token.'
            raise AuthError(error, 400)

    # expected key not found
    error['code'] = 'invalid_header'
    error['description'] = 'Unable to find the appropriate key.'
    raise AuthError(error, 400)


'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
