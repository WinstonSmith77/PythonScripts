from assertpy import assert_that

def mult(a, b):
    if b < 0:
        a = -a
        b = -b
    prod = 0
    while b > 0:
        b -= 1
        prod += a
    return prod


assert_that(mult(-3, -4)).is_equal_to(3*4)
assert_that(mult(3, -4)).is_equal_to(3*(-4))
assert_that(mult(-3, 4)).is_equal_to(-3*4)
assert_that(mult(3, 0)).is_equal_to(0)
assert_that(mult(0, 3)).is_equal_to(0)
assert_that(mult(0.3, 3)).is_close_to(0.9, 1e-12)
