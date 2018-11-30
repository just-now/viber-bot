from request import Request
from rutils import RequestPayloadUT
import request2
import unittest
import asyncio

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class RequestHandler(object):

    def __init__(self):
        self._req_map = {}
        self._loop = asyncio.get_event_loop()

    def find_by_vid(self, vid):
        """Finds request inside reqh queues by viber id `vid'"""
        return self._req_map.get(vid)

    def new(self, vid):
        """Creates new request and appends it into reqh queues"""
        self._req_map[vid] = Request(self._loop)
        return self._req_map[vid]

    def delete(self, vid):
        """Deletes request from reqh queues"""
        self._req_map.pop(vid)

    def send(self, rq):
        print(bcolors.WARNING+"<<<")
        print(rq.get_user_id())
        print(rq.get_message_out())
        print(rq.get_kbd().to_ut_str())
        print(">>>"+bcolors.ENDC)

    def process(self, payload):
        rq = self.find_by_vid(payload.user_id())

        if rq is None:
            rq = self.new(payload.user_id())

        if rq.advance(payload):
            self.send(rq)

        if rq.finished():
            self.delete(payload.user_id())

class TestRequestHandler(unittest.TestCase):

    def incoming(self, reqh, payload):
        reqh.process(payload)

    def test_XXX(self):
        reqh = RequestHandler()

        # 1
        # self.incoming(reqh, RequestPayloadUT([0,0,0,1]))
        # self.incoming(reqh, RequestPayloadUT([0,0,0,2]))
        # self.incoming(reqh, RequestPayloadUT([0,0,0,1]))
        # self.incoming(reqh, RequestPayloadUT([0,0,0,2]))

        # 2
        self.incoming(reqh, RequestPayloadUT(["ViberConversationStartedRequest",
                                              "", "time_12:00", "22322"]))
        self.incoming(reqh, RequestPayloadUT(["ViberMessageRequest",
                                              "{{"+"Register"+"}}", "time_12:01", "22322"]))
        self.incoming(reqh, RequestPayloadUT(["ViberMessageRequest",
                                              "+38066-7176666", "time_12:01", "22322"]))
        self.incoming(reqh, RequestPayloadUT(["ViberMessageRequest",
                                              "{{"+"Register"+"}}", "time_12:01", "22322"]))
        self.incoming(reqh, RequestPayloadUT(["ViberMessageRequest",
                                              "+380667176666", "time_12:01", "22322"]))
        self.incoming(reqh, RequestPayloadUT(["ViberMessageRequest",
                                              "{{"+"AddHomeFlat"+"}}", "time_12:01", "22322"]))
        self.incoming(reqh, RequestPayloadUT(["ViberMessageRequest",
                                              "4д,197", "time_12:01", "22322"]))
        self.incoming(reqh, RequestPayloadUT(["ViberMessageRequest",
                                              "{{"+"AddName"+"}}", "time_12:01", "22322"]))
        self.incoming(reqh, RequestPayloadUT(["ViberMessageRequest",
                                              "Vasiliy", "time_12:01", "22322"]))
        self.incoming(reqh, RequestPayloadUT(["ViberMessageRequest",
                                              "{{"+""+"}}", "time_12:01", "22322"]))
        self.incoming(reqh, RequestPayloadUT(["ViberMessageRequest",
                                              "{{"+"AddCar"+"}}", "time_12:01", "22322"]))
        self.incoming(reqh, RequestPayloadUT(["ViberMessageRequest",
                                              "VN1929VV", "time_12:01", "22322"]))

if __name__ == '__main__':
    unittest.main()
