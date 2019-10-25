from my_python_package.Modifys import restore, run_time


@run_time
@restore(3, (AssertionError,))
def demo(s: int):
    assert s > 5


if __name__ == '__main__':
    demo(1)