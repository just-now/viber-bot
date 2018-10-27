import request
import unittest

class RequestHandler(object):

    def __init__(self):
        self._req_queue = {}

    def find_request_by_vid(self, vid):
        """Finds request inside reqh queues by viber id `vid'"""
        return self._req_queue.get(vid)

    def new_request(self, vid, payload):
        """Creates new request and appends it into reqh queues"""
        self._req_queue[vid] = Request(payload)

    def del_request(self, vid):
        """Deletes request from reqh queues"""
        self._req_queue.pop(vid)


class TestRequestHandler(unittest.TestCase):
    def test_XXX(self):
        pass

if __name__ == '__main__':
    unittest.main()
