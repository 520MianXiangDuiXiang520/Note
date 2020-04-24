import asyncio
import time


async def run(delay: int):
    await asyncio.sleep(delay)
    print(f"After {delay} seconds,end of operation")


async def main():
    coroutine1 = run(6)
    coroutine2 = run(4)
    task1 = asyncio.create_task(coroutine1)
    task2 = asyncio.create_task(coroutine2)
    await task1
    await task2


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    print(f"run with {time.time() - start}")

