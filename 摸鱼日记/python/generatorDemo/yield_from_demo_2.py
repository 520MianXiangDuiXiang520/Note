def average():
    total = 0
    nums = 0
    result = 0
    while True:
        get_num = yield
        if not get_num:
            break
        total += get_num
        nums += 1
        result = total / nums
    print("算完了")
    return result


def middle(gen):
    while True:
        result = yield from gen()
        print(result)


def main():
    m = middle(average)
    m.send(None)  # 初激
    for v in [12, 25, 48]:
        m.send(v)
    m.send(None)


if __name__ == '__main__':
    main()