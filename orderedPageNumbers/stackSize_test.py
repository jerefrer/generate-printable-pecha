from orderedPageNumbers.orderedPageNumbers import stackSize

def test_1():
    assert stackSize(1) == 1

def test_2():
    assert stackSize(2) == 2

def test_3():
    assert stackSize(3) == 2

def test_4():
    assert stackSize(4) == 2

def test_5():
    assert stackSize(5) == 2

def test_6():
    assert stackSize(6) == 2

def test_7():
    assert stackSize(7) == 4

def test_8():
    assert stackSize(8) == 4

def test_9():
    assert stackSize(9) == 4

def test_10():
    assert stackSize(10) == 4

def test_11():
    assert stackSize(11) == 4

def test_12():
    assert stackSize(12) == 4

def test_13():
    assert stackSize(13) == 6

def test_14():
    assert stackSize(14) == 6
