import requests

from datetime import datetime

from .exc import ApiException
from .utils import iso_parse


API_V1 = 'api/v1/'


class AuthenticationError(Exception):

    pass


class AuthArgs:

    def __init__(self, json=None, headers=None) -> None:
        self.json = None
        self.headers = None


class Authentication:

    def authenticate(self, url_base: str):
        raise NotImplementedError

    def auth_args(self) -> AuthArgs:
        raise NotImplementedError

    @staticmethod
    def check_auth_resp(resp) -> None:
        if resp.status_code != 200:
            msg = None
            data = resp.json()
            if data is not None:
                msg = data.get('message', None)
            if msg is None:
                msg = 'Unknown error'
            raise AuthenticationError(msg)
        
        try:
            return resp.json()
        except ValueError:
            raise ApiException('API response not JSON: {}'.format(resp.text))


class AuthToken(Authentication):

    def __init__(self, auth_token: str, expires: datetime) -> None:
        self.auth_token = auth_token

    @classmethod
    def from_json(cls, json_resp: dict):
        try:
            token = json_resp['token']
        except KeyError:
            raise ApiException('Response missing field "token"')

        try:
            expires = json_resp['expires']
        except KeyError:
            raise ApiException('Response missing field "expires"')
        
        try:
            expires = iso_parse(expires)
        except ValueError as e:
            raise ApiException(str(e))

        return AuthToken(token, expires)

    def authenticate(self, url_base: str):
        resp = requests.get(url_base + API_V1 + 'token',
                            headers={'Accept': 'application/json',
                                     'Content-Type': 'application/json',
                                     'Authentication': 'Token {}'.format(self.auth_token)})
        self.check_auth_resp(resp)
        return Authentication


class UserPassOtp(Authentication):

    def __init__(self, username: str, passphrase: str, one_time_code: str) -> None:
        self.username = username
        self.passphrase = passphrase
        self.one_time_code = one_time_code

    def authenticate(self, url_base: str) -> Authentication:
        resp = requests.get(url_base + API_V1 + 'token',
                            headers={'Accept': 'application/json',
                                     'Content-Type': 'application/json'},
                            data={'username': self.username,
                                  'passphrase': self.passphrase,
                                  'one_time_code': self.one_time_code},
                            allow_redirects=True)
        data = self.check_auth_resp(resp)
        return AuthToken.from_json(data)
