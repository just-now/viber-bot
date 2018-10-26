from enum import Enum

# ---
class RequestType(Enum):
    MESSAGE_REQUEST              = 1
    CONVERSATION_STARTED_REQUEST = 2
    _str_rq_to_typed = {
        "MESSAGE_REQUEST"              : MESSAGE_REQUEST,
        "CONVERSATION_STARTED_REQUEST" : CONVERSATION_STARTED_REQUEST
    }

    @staticmethod
    def to_enum(str_rqtype):
        return _str_rq_to_typed[str_rqtype]

# ---
class RequestPayloadUT(object):
    def __init__(self, payload):
        self._payload = payload
    def type(self):
        return RequestType.to_enum(self._payload[0])
    def text(self):
        return self._payload[1]
    def time(self):
        return self._payload[2]
    def user_id(self):
        return self._payload[3]
