import requests

from typing import Union

from . import __version__, API_V1
from .auth import Authentication
from .data import Sources, Source, Submissions, Submission, Reply, User
from .exc import ApiException

'''HTTP client
'''


class Client:
    '''An HTTP client that interacts with the SecureDrop API.
    '''

    def __init__(self, url_base: str, authentication: Authentication, user_agent: str=None) -> None:
        ''':param url_base: URL of the SecureDrop
           :param authentication: A :class:`.auth.Authentication` used to perfor the initial
                                  authentication.
           :param user_agent: An optional string that will be used to genreate the ``User-Agen``
                              header
        '''
        if not url_base.endswith('/'):
            url_base = url_base + '/'
        self.url_base = url_base

        self.authentication = authentication.authenticate(url_base)

        if user_agent:
            self.user_agent = '{} (python-securedrop-api/{})'.format(user_agent, __version__)
        else:
            self.user_agent = 'python-securedrop-api/{}'.format(__version__)

    def __request(self, method=None, path=None, json=None, headers=None):
        _headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': self.user_agent,
        }
        if headers:
            _headers.update(**headers)

        auth = self.authentication.auth_args()
        if json is None:
            json = auth.json

        if auth.headers:
            _headers.update(**auth.headers)

        url = '{}{}{}'.format(self.url_base, API_V1, path)
        return requests.request(
            method=method,
            url=url,
            json=json,
            headers=_headers,
            allow_redirects=True)

    def sources(self) -> Sources:
        '''Get an object containing information about all sources.
           Correponds to ``GET /api/v1/sources``
        '''
        resp = self.__request('GET', 'sources')
        if resp.status_code != 200:
            raise ApiException('Unexpected response: {} {}'.format(resp.status_code, resp.text))

        try:
            resp_json = resp.json()
        except ValueError:
            raise ApiException('Response was not JSON: {}'.format(resp.text))

        return Sources.from_json(resp_json)

    def source(self, uuid: Union[UUID, str]) -> Source:
        '''Return a single source.
           Correponds to ``GET /api/v1/sources/<uuid:uuid>``
           :param uuid: The source's ``uuid``
        '''
        resp = self.__request('GET', 'sources/{}'.format(uuid))
        if resp.status_code != 200:
            raise ApiException('Unexpected response: {} {}', resp.status_code, resp.text)

        try:
            source = resp.json()
        except ValueError:
            raise ApiException('Response was not JSON: {}'.format(resp.text))

        return Source.from_json(source)

    def source_submissions(self, uuid: Union[UUID, str]) -> Submissions:
        '''Return on object containing information about all submission for a given source.
           Correponds to ``GET /api/v1/sources/<uuid:uuid>/submissions``
           :param uuid: The source's ``uuid``
        '''
        resp = self.__request('GET', 'sources/{}/submissions'.format(uuid))
        if resp.status_code != 200:
            raise ApiException('Unexpected response: {} {}'.format(resp.status_code, resp.text))

        try:
            resp_json = resp.json()
        except ValueError:
            raise ApiException('Response was not JSON: {}'.format(resp.text))

        return Submissions.from_json(resp_json)

    def source_submission(self, uuid: Union[UUID, str], submission_id: int) -> Submission:
        '''Return on object containing information about all submission for a given source.
           Correponds to ``GET /api/v1/sources/<uuid:uuid>/submissions/<int:submission_id>``
           :param uuid: The source's ``uuid``
           :param submission_id: The submissions's id
        '''
        resp = self.__request('GET',
                              'sources/{}/submissions/{}'.format(uuid, submission_id))
        if resp.status_code != 200:
            raise ApiException('Unexpected response: {} {}', resp.status_code, resp.text)

        try:
            source = resp.json()
        except ValueError:
            raise ApiException('Response was not JSON: {}'.format(resp.text))

        return Submission.from_json(source)

    def delete_source_submission(self, uuid: Union[UUID, str], submission_id: int) -> None:
        '''Delete a source's submission.
           Correponds to
           ``DELETE /api/v1/sources/<uuid:uuid>/submissions/<int:submission_id>``
           :param uuid: The source's ``uuid``
           :param submission_id: The submissions's id
        '''
        resp = self.__request('GET',
                              'sources/{}/submissions/{}'.format(uuid, submission_id))
        if resp.status_code != 200:
            raise ApiException('Unexpected response: {} {}', resp.status_code, resp.text)

    def delete_source(self, uuid: Union[UUID, str]) -> None:
        '''Delete a source and all their submissions.
           Correponds to ``DELETE /api/v1/sources/<uuid:uuid>``
           :param uuid: The source's ``uuid``
        '''
        resp = self.__request('GET', 'sources/{}'.format(uuid))
        if resp.status_code != 200:
            raise ApiException('Unexpected response: {} {}', resp.status_code, resp.text)

    def reply_to_source(self, uuid: Union[UUID, str], reply: Reply) -> None:
        '''Send a reply to a source.
           Correponds to ``POST /api/v1/sources/<uuid:uuid>/reply``
           :param uuid: The source's ``uuid``
           :param reply: A reply object.
        '''
        if not isinstance(reply, Reply):
            raise TypeError('Can only send `Reply` objects.')

        resp = self.__request('POST',
                              'sources/{}/reply'.format(uuid),
                              json=reply.to_json())
        if resp.status_code != 200:
            raise ApiException('Unexpected response: {} {}', resp.status_code, resp.text)

    def star_source(self, uuid: Union[UUID, str]) -> None:
        '''Add a star to a source.
           Correponds to ``POST /api/v1/sources/<uuid:uuid>/star``
           :param uuid: The source's ``uuid``
        '''
        resp = self.__request('POST', 'sources/{}/star'.format(uuid))
        if resp.status_code != 200:
            raise ApiException('Unexpected response: {} {}', resp.status_code, resp.text)

    def unstar_source(self, uuid: Union[UUID, str]) -> None:
        '''Remote a star from a source.
           Correponds to ``DELETE /api/v1/sources/<uuid:uuid>/star``
           :param uuid: The source's ``uuid``
        '''
        resp = self.__request('POST', 'sources/{}/star'.format(uuid))
        if resp.status_code != 200:
            raise ApiException('Unexpected response: {} {}', resp.status_code, resp.text)

    def user(self) -> User:
        '''Information about the current authenticated user.
           Correponds to ``GET /api/v1/user``.
        '''
        resp = self.__request('GET', 'user')
        if resp.status_code != 200:
            raise ApiException('Unexpected response: {} {}', resp.status_code, resp.text)

        try:
            user = resp.json()
        except ValueError:
            raise ApiException('Response was not JSON: {}'.format(resp.text))

        return User.from_json(user)
