import multiprocessing
import sys
from my_python_package import Modifys
# d = 8128751813
e = 17
p = 473398607161
q = 4511491


def p1(d, end):
    m = (p-1)*(q-1)
    while True:
        d += 1
        print(d)
        if (d * e) % m == 1 or d == end:
            print("**********" + repr(d))
            sys.exit(1)

if __name__ == '__main__':
    s1 = multiprocessing.Process(target=p1, args=(8172377987, 8539575482))
    s2 = multiprocessing.Process(target=p1, args=(8572284325, 9128751813,))
    s3 = multiprocessing.Process(target=p1, args=(9172254188, 9539499456,))
    s4 = multiprocessing.Process(target=p1, args=(9572273545, 10000000000))
    s1.start()
    s2.start()
    s3.start()
    s4.start()

