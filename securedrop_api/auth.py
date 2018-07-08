import json as json_
import requests

from json_serde import JsonSerde, String, IsoDateTime

from . import API_V1
from .exc import ApiException

'''Helpers for authentication
'''


class AuthenticationError(Exception):
    '''Generic error raised on authentication failure.
    '''

    pass


class AuthArgs:
    '''Data type for HTTP additions that may be used during authentication.
    '''

    def __init__(self, json: dict=None, headers: dict=None) -> None:
        ''':param json: JSON body
           :param headers: Addtional HTTP headers
        '''
        self.json = json
        self.headers = headers


class Authentication:
    '''Abstract class for authentication.
    '''

    def authenticate(self, url_base: str):
        ''':param url_base: The SecureDrop API base URL
        '''
        raise NotImplementedError

    def auth_args(self) -> AuthArgs:
        raise NotImplementedError

    @staticmethod
    def check_auth_resp(resp) -> None:
        if resp.status_code != 200:
            msg = None
            try:
                data = resp.json()
            except ValueError:
                data = None
            if data is not None:
                msg = data.get('message', None)
            if msg is None:
                msg = 'Unknown error'
            raise AuthenticationError(msg)

        try:
            return resp.json()
        except ValueError:
            raise ApiException('API response not JSON: {}'.format(resp.text))


class AuthToken(Authentication, JsonSerde):

    token = String()
    expiration = IsoDateTime()

    def auth_args(self) -> AuthArgs:
        return AuthArgs(headers={'Authorization': 'Token {}'.format(self.token)})

    def authenticate(self, url_base: str) -> Authentication:
        resp = requests.post(url_base + API_V1 + 'token',
                             headers={'Accept': 'application/json',
                                      'Content-Type': 'application/json',
                                      'Authorization': 'Token {}'.format(self.token)})
        self.check_auth_resp(resp)
        return Authentication


class UserPassOtp(Authentication):

    def __init__(self, username: str, passphrase: str, one_time_code: str) -> None:
        self.username = username
        self.passphrase = passphrase
        self.one_time_code = one_time_code

    def auth_args(self) -> AuthArgs:
        return AuthArgs(json={'username': self.username,
                              'passphrase': self.passphrase,
                              'one_time_code': self.one_time_code})

    def authenticate(self, url_base: str) -> Authentication:
        resp = requests.post(url_base + API_V1 + 'token',
                             headers={'Accept': 'application/json',
                                      'Content-Type': 'application/json'},
                             data=json_.dumps({'username': self.username,
                                               'passphrase': self.passphrase,
                                               'one_time_code': self.one_time_code}),
                             allow_redirects=True)
        data = self.check_auth_resp(resp)
        return AuthToken.from_json(data)
