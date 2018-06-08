import asyncio
import random


class Potato:
    @classmethod
    def make(cls, num, *args, **kwargs):
        potatos = []
        for i in range(num):
            potatos.append(cls.__new__(cls))
        return potatos


all_potatos = Potato.make(5)


async def ask_for_potato():
    await asyncio.sleep(random.random())
    all_potatos.extend(Potato.make(random.randint(1, 10)))


async def take_potatos(num):
    count = 0
    while True:
        if len(all_potatos) == 0:
            await ask_for_potato()
        else:
            potato = all_potatos.pop()
            yield potato
            count += 1
            if count == num:
                break


async def buy_potatos():
    bucket = [p async for p in take_potatos(50)]


def main():
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(buy_potatos())
    loop.close()


if __name__ == "__main__":
    main()