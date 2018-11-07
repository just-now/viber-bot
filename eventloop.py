import asyncio
import unittest



async def co_first_nested(idx, m, loop):
    m[idx] = loop.create_future()
    print(idx + "N1", flush=True)
    loop.stop()
    await m[idx]
    print(idx + "N2", flush=True)


async def co_first(idx, m):
    print(idx + "1", flush=True)
    loop = asyncio.get_running_loop()
    m[idx] = loop.create_future()
    loop.stop()
    await m[idx]
    print(idx + "2", flush=True)

    await co_first_nested(idx, m, loop)
    #
    loop.stop()


def process():
    loop = asyncio.get_event_loop()
    m = {}
    task1 = loop.create_task(co_first("task 1: ", m))
    task2 = loop.create_task(co_first("task 2: ", m))
    loop.run_forever()

    m["task 1: "].set_result(11)
    m["task 2: "].set_result(22)
    loop.run_forever()

    m["task 1: "].set_result(11)
    m["task 2: "].set_result(22)
    loop.run_forever()
    print(asyncio.all_tasks(loop))


class TestEventLoop(unittest.TestCase):
    process()

if __name__ == '__main__':
    unittest.main()
