import asyncio
import unittest

class EventLoop(object):
    async def co_first_nested(self, idx, m, loop):
        m[idx] = loop.create_future()
        print(idx + "N1", flush=True)
        loop.stop()
        await m[idx]
        #raise ValueError("123")
        print(idx + "N2", flush=True)
        return "112233"


    async def co_first(self, idx, m, loop):
        try:
            print(idx + "1", flush=True)
            m[idx] = loop.create_future()
            loop.stop()
            await m[idx]
            print(idx + "2", flush=True)

            x = await self.co_first_nested(idx, m, loop)
            print("###"+x)
            #
            loop.stop()
        except Exception as e:
            print ("Failed with {}".format(e))
            await m[idx]
            loop.stop()

    def process(self):
        loop = self.loop
        m = {}
        task1 = loop.create_task(self.co_first("task 1: ", m, loop))
        task2 = loop.create_task(self.co_first("task 2: ", m, loop))
        loop.run_forever()

        print("---");
        m["task 1: "].set_result(11)
        m["task 2: "].set_result(22)
        loop.run_forever()

        print("---");
        m["task 1: "].set_result(11)
        m["task 2: "].set_result(22)
        loop.run_forever()
        print("---");

    def __init__(self, loop):
        self.loop = loop

class TestEventLoop(unittest.TestCase):
    def test_XXX(self):
        loop = asyncio.get_event_loop()
        ev = EventLoop(loop)
        ev.process()

if __name__ == '__main__':
    unittest.main()
