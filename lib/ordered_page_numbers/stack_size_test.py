from ordered_page_numbers.ordered_page_numbers import stack_size

def test_1():
    assert stack_size(1) == 1

def test_2():
    assert stack_size(2) == 2

def test_3():
    assert stack_size(3) == 2

def test_4():
    assert stack_size(4) == 2

def test_5():
    assert stack_size(5) == 2

def test_6():
    assert stack_size(6) == 2

def test_7():
    assert stack_size(7) == 4

def test_8():
    assert stack_size(8) == 4

def test_9():
    assert stack_size(9) == 4

def test_10():
    assert stack_size(10) == 4

def test_11():
    assert stack_size(11) == 4

def test_12():
    assert stack_size(12) == 4

def test_13():
    assert stack_size(13) == 6

def test_14():
    assert stack_size(14) == 6
