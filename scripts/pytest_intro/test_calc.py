#def test_add_calc():
#    assert 100 + 100 == 200

def add_calc(num1 , num2):
    return num1 + num2

def test_add_calc():
    assert add_calc(99, 1) == 100
    assert add_calc(-1, 1) == 0
    assert add_calc(-3, 0) == -3
    assert add_calc(1000, 3000) == 4000

