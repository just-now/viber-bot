from request import Request
from rutils import RequestPayloadUT
import request
import unittest

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
        self._req_queue = {}

    def find_by_vid(self, vid):
        """Finds request inside reqh queues by viber id `vid'"""
        return self._req_queue.get(vid)

    def new(self, vid, payload):
        """Creates new request and appends it into reqh queues"""
        self._req_queue[vid] = Request(payload)
        return self._req_queue[vid]

    def delete(self, vid):
        """Deletes request from reqh queues"""
        self._req_queue.pop(vid)

    def send(self, rq):
        print(bcolors.WARNING+"<<<")
        print(rq.get_user_id())
        print(rq.get_message_out())
        print(rq.get_kbd().to_ut_str())
        print(">>>"+bcolors.ENDC)

    def process(self, payload):
        rq = self.find_by_vid(payload.user_id())
        if rq is None:
            rq = self.new(payload.user_id(), payload)
        else:
            rq.update_payload(payload)

        while True:
            rq.advance()
            if rq.need_output():
                self.send(rq)
            if rq.need_input():
                break

        if rq.finished():
            self.delete(payload.user_id())

#---- ##############################

def _called_by_incoming1(rq):
    yield rq.context

def _called_by_incoming2(rq):
    yield rq.context

def _incoming(rq):
    _called_by_incoming1(rq)
    _called_by_incoming2(rq)

def main():
    rq = Rq()
    rq.context = _incoming(rq)
    #     _called_by_incoming1(rq) called
    rq.context = next(rq.context)
    #     _called_by_incoming2(rq) called

#---- ##############################

class TestRequestHandler(unittest.TestCase):

    def incoming(self, reqh, payload):
        reqh.process(payload)

    def test_XXX(self):
        reqh = RequestHandler()
        # inside ViberConversationStartedRequest
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
