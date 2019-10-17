from contextlib import contextmanager, suppress
from contextlib import closing
import contextlib
from urllib.request import urlopen

@contextmanager
def my_open(path: str, mode: str):
    fp = open(path, mode)
    try:
        yield fp
    finally:
        print("close file")
        fp.close()


if __name__ == '__main__':
    with suppress(OSError):
        with my_open('01.txt', 'r') as fp:
            raise OSError
            fp.write("111")

    # myfunction()

