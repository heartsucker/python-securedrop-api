from securedrop_api.data import Sources, Source, User


def test_sources_serde():
    json = {
        'sources': [
            {
                'source_id': 1,
                'filesystem_id': 'abc',
                'journalist_designation': 'foo bar',
                'flagged': True,
                'last_updated': '2018-01-01T00:00:00Z',
                'number_of_messages': 2,
                'number_of_documents': 3,
                'interaction_count': 4,
            },
        ],
    }

    sources = Sources.from_json(json)
    assert sources.sources[0].filesystem_id == json['sources'][0]['filesystem_id']


def test_source_serde():
    json = {
        'source_id': 1,
        'filesystem_id': 'abc',
        'journalist_designation': 'foo bar',
        'flagged': True,
        'last_updated': '2018-01-01T00:00:00Z',
        'number_of_messages': 2,
        'number_of_documents': 3,
        'interaction_count': 4,
    }

    source = Source.from_json(json)
    assert source.filesystem_id == json['filesystem_id']


def test_user_serde():
    json = {
        'user': {
            'is_admin': True,
            'last_login': '2018-01-01T00:00:00Z',
            'username': 'journalist',
        },
    }

    user = User.from_json(json)
    assert user.username == json['user']['username']
