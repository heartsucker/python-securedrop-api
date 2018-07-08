from datetime import datetime

from json_serde import JsonSerde, String, Integer, IsoDateTime, List, Boolean, Nested


class Source(JsonSerde):

    source_id = Integer()
    filesystem_id = String()
    journalist_designation = String()
    last_updated = IsoDateTime()
    flagged = Boolean()
    interaction_count = Integer()
    number_of_documents = Integer()
    number_of_messages = Integer()


class Sources(JsonSerde):

    sources = List(Source)


class Submission(JsonSerde):

    submission_id = Integer()
    filename = String()
    is_read = Boolean()
    size = Integer()


class Submissions(JsonSerde):

    submissions = List(Submission)


class Reply:

    def __init__(self, reply: str) -> None:
        self.reply = reply

    @property
    def reply(self) -> str:
        return self.__reply

    @reply.setter
    def reply(self, reply: str) -> None:
        if not (reply.startswith('-----BEGIN PGP MESSAGE----')
                and reply.endswith('-----END PGP MESSAGE-----')):
            raise ValueError('Reply was not pre-encrypted')
        self.__reply = reply

    @reply.deleter
    def reply(self) -> None:
        raise NotImplementedError('Cannot delete a reply.')

    def to_json(self) -> dict:
        return {'reply': self.__reply}


class UserInner(JsonSerde):

    username = String()
    is_admin = Boolean()
    last_login = IsoDateTime()


class User(JsonSerde):

    __user = Nested(UserInner, rename='user')

    @property
    def username(self) -> str:
        return self.__user.username

    @username.setter
    def username(self, value: str) -> None:
        self.user.__username = value

    @property
    def is_admin(self) -> bool:
        return self.__user.is_admin

    @is_admin.setter
    def is_admin(self, value: bool) -> None:
        self.__user.is_admin = value

    @property
    def last_login(self) -> datetime:
        return self.__user.last_login

    @last_login.setter
    def last_login(self, value: datetime) -> None:
        self.__user.last_login = value
