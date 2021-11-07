"""
Module with function multiply_by_2 and its tests
"""


def multiply_by_2(num: int) -> int or str:
    """
    Function returns integer <num> multiplied by 2.
    """

    if isinstance(num, int):
        return 2 * num
    return 'Error!!! Argument <num> must be integer!!!'


def test_correct_multiply():
    assert multiply_by_2(2) == 4, 'Correct multiply is not true!'


def test_correct_multiply_negative():
    assert multiply_by_2(-2) != -5, 'Correct multiply is not true!'


def test_incorrect_multiply():
    assert multiply_by_2(2) != 5, 'Incorrect multiply is not true!'


def test_incorrect_multiply_by_str():
    assert multiply_by_2("str") == 'Error!!! Argument <num> must be integer!!!', \
        'Wrong answer if <num> is not integer!'


# def test_correct_multiply_negative():
#     assert multiply_by_2(-2) == -4, 'Correct multiply by negative is not true!'


def test_correct_multiply_by_zero():
    assert multiply_by_2(0) == 0, 'Multiply by zero is not equal zero!'




def test_incorrect_multiply():
    assert multiply_by_2(2) != 5, 'Incorrect multiply is not true!'



def test_incorrect_multiply_by_float():
    assert multiply_by_2(0.1) == 'Error!!! Argument <num> must be integer!!!', \
        'Wrong answer if <num> is not integer!'


print(multiply_by_2(5))


if __name__ == "__main__":
    test_correct_multiply()
    # test_incorrect_multiply()
    # test_correct_multiply_by_zero()
    # test_incorrect_multiply_by_float()
