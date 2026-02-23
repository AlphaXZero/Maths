import numpy


def code_xor(message, key):
    return "".join(
        [str(int(m_char) ^ int(k_char)) for m_char, k_char in zip(message, key)]
    )


def do_exercise1():
    message = "10110101"
    key = "11001010"
    print(f"message: {message} key: {key}")
    print(f"coded message : {code_xor(key, message)}")
    print(f"decoded message : {code_xor(code_xor(key, message), key)}")


if __name__ == "__main__":
    print(do_exercise1())
