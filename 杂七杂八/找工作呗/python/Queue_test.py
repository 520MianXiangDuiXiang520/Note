from concurrent.futures import ThreadPoolExecutor
from time import sleep
from queue import SimpleQueue


def get_html(name):
    sleep(2)
    print(f"{name} get ok")


if __name__ == '__main__':
    executor = ThreadPoolExecutor(max_workers=2)
    task1 = executor.submit(get_html, ("first", ))
    task2 = executor.submit(get_html, ("second",))
    # print(task1.done())
