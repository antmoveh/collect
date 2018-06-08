import asyncio


future = asyncio.Future()


async def corol():
    await asyncio.sleep(1)
    future.set_result('data')


async def coro2():
    print(await future)

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait([corol(), coro2()]))
loop.close()


