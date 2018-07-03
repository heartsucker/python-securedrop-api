from datetime import datetime

from .exc import ApiException
from .utils import iso_parse

class Source

    # TODO public key
    def __init__(self,
                 filesystem_id: str,
                 is_flagged: bool,
                 interaction_count: int,
                 journalist_designation: str,
                 last_updated: datetime,
                 number_of_documents: int,
                 number_of_messages: int,
                 source_id: int) -> None:
        self.filesystem_id = filesystem_id
        self.is_flagged = is_flagged
        self.interaction_count = interaction_count
        self.journalist_designation = journalist_designation
        self.last_updated = last_updated
        self.number_of_documents = number_of_documents
        self.number_of_messages = number_of_messages
        self.source_id = source_id

    @classmethod
    def from_json(cls, data):
        try:
            filesystem_id = data['filesystem_id']
        except KeyError:
            raise ApiException('Field "filesystem_id" missing from response.')

        try:
            flagged = data['flagged']
        except KeyError:
            raise ApiException('Field "flagged" missing from response.')

        try:
            interaction_count = data['interaction_count']
        except KeyError:
            raise ApiException('Field "interaction_count" missing from response.')

        try:
            journalist_designation = data['journalist_designation']
        except KeyError:
            raise ApiException('Field "journalist_designation" missing from response.')

        try:
            last_updated = data['last_updated']
        except KeyError:
            raise ApiException('Field "last_updated" missing from response.')

        try:
            last_updated = iso_parse(last_updated)
        except ValueError as e:
            raise ApiException('Field "last_updated" had bad format: {}'.format(e))

        try:
            number_of_documents = data['number_of_documents']
        except KeyError:
            raise ApiException('Field "number_of_documents" missing from response.')

        try:
            number_of_messages = data['number_of_messages']
        except KeyError:
            raise ApiException('Field "number_of_messages" missing from response.')

        try:
            source_id = data['source_id']
        except KeyError:
            raise ApiException('Field "source_id" missing from response.')

        return cls(filesystem_id,
                   flagged,
                   interaction_count,
                   journalist_designation,
                   last_updated,
                   number_of_documents,
                   number_of_messages,
                   source_id)
