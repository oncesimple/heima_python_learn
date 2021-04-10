num = 100
nums = [11, 22]


def test1():
    global num
    num += 100


def test2():
    nums.append(33)


def main():
    print(num)
    print(nums)

    test1()
    test2()

    print(num)
    print(nums)

    pass


if __name__ == '__main__':
    main()
