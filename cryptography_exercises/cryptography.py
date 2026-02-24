import numpy


def code_xor(message, key):
    return "".join(
        [str(int(m_char) ^ int(k_char)) for m_char, k_char in zip(message, key)]
    )


def has_not_common_divisor(a, b):
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            return 0
    return 1


def do_bbs(p, q, x0, ammount):
    """
    p and q % 3 == 4
    x0 should have no common divisor with m and must not be equal to 0 or 1
    """
    if not (p % 4 == 3 and q % 4 == 3):
        return -1
    m = p * q
    if not has_not_common_divisor(m, x0):
        return -1
    result = ""
    for i in range(ammount):
        x0 = x0**2 % 253
        result += str(bin(x0))[-1]
    return result


def do_exercise1():
    message = "10110101"
    key = "11001010"
    print(f"message: {message} key: {key}")
    print(f"coded message : {code_xor(key, message)}")
    print(f"decoded message : {code_xor(code_xor(key, message), key)}")


def do_exercise2():
    print(do_bbs(7, 11, 5, 5))
    print(do_bbs(2027, 2039, 3, 10))


if __name__ == "__main__":
    # do_exercise1()
    do_exercise2()
