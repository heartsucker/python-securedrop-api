from securedrop_api.auth import AuthToken


def test_parse_resp():
    json_resp = {'token': 'foobar',
                 'expiration': '2018-01-01T00:00:00Z'}
    AuthToken.from_json(json_resp)
