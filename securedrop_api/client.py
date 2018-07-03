from . import __version__
from .auth import Authentication
from .data import Source


class Client:

    def __init__(self, url_base: str, authentication: Authentication, user_agent: str=None) -> None:
        if not url_base.ends_with('/'):
            url_base = url_base + '/'
        self.url_base = url_base

        self.authentication = authentication.authenticate()

        if user_agent:
            self.user_agent = '{} (python-securedrop-api/{})'.format(user_agent, __version__)
        else:
            self.user_agent = 'python-securedrop-api/{}'.format(__version__)

    def __request(self, method=None, url=None, json=None, headers=None):
        _headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': self.user_agent,
        }
        if headers:
            _headers.update(headers)

        auth = self.authentication.auth_args()
        json = auth.json or json
        if auth.headers:
            _headders.update(headers)

        return requests.request(
            method=method,
            url=url,
            json=json,
            headers=_headers,
            allow_redirects=True)

    def sources(self) -> list:
        resp = self.__request('GET', 'sources')
        if resp.status_code != 200:
            raise ApiException('Unexpected response: {} {}', resp.status_code, resp.text)

        try:
            sources = resp.json()
        except ValueError:
            raise ApiException('Response was not JSON: {}'.format(resp.text))

        out = []
        for source in resp_json:
            out.append(Source.from_json(source))
        return out

    def source(self, filesystem_id: str) -> list:
        resp = self.__request('GET', 'sources/{}'.format(filesystem_id))
        if resp.status_code != 200:
            raise ApiException('Unexpected response: {} {}', resp.status_code, resp.text)

        try:
            source = resp.json()
        except ValueError:
            raise ApiException('Response was not JSON: {}'.format(resp.text))

        return Source.from_json(source)
