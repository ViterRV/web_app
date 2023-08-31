import asyncio

async def send_one():
    n = 0
    while True:
        await asyncio.sleep(1)
        n+=1
        if n%3 !=0:
            print(f'прийшло{n} секунд')


async def send_tree():
    while True:
        await asyncio.sleep(3)
        print(f'пройшло ще 3 секунди')


async def main():
    tasl_1 = asyncio.create_task(send_one())
    tasl_2 = asyncio.create_task(send_tree())
    await tasl_1
    await tasl_2
asyncio.run(main())