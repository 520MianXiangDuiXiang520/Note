final_result = {}


def calculate():
    total = 0
    nums = []
    while True:
        info = yield
        if not info:
            break
        total += info
        nums.append(info)
    return total, nums


def middle(key: str, gen):
    while True:
        final_result[key] = yield from gen()
        print(final_result)


def main():
    data = {
        "apple": [230, 569, 234, 776],
        "banana": [564, 213, 798, 327],
        "strawberry": [98, 76, 120, 436, 55],
        "orange": [78, 67, 345, 124]
    }
    for key, value in data.items():
        mid = middle(key, calculate)
        mid.send(None)  # 初激
        for v in value:
            mid.send(v)
        mid.send(None)


if __name__ == '__main__':
    main()
