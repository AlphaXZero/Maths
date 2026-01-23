import numpy as np
from scipy.signal import convolve2d, convolve
from PIL import Image


def do_convolution(matrix: np.ndarray, pattern: np.ndarray):
    """
    The pattern is flipped and zeros are added around the matrix to avoid
    out of range errors. Then it's a simple coefficient calculation.
    Inserts should be changed to something else because it could breaks if the pattern is too big
    """
    output = np.zeros(matrix.shape)
    pattern = np.flip(pattern)
    matrix = np.insert(matrix, 0, np.zeros((matrix.shape[1])), axis=0)
    matrix = np.insert(matrix, 0, np.zeros((matrix.shape[0])), axis=1)
    matrix = np.insert(matrix, matrix.shape[0], np.zeros((matrix.shape[1])), axis=0)
    matrix = np.insert(matrix, matrix.shape[1], np.zeros((matrix.shape[0])), axis=1)
    for i in range(1, matrix.shape[0] - 1):
        for j in range(1, matrix.shape[1] - 1):
            actual_sum = 0
            for y in range(pattern.shape[0]):
                for x in range(pattern.shape[1]):
                    actual_sum += matrix[i - (1 - y), j - (1 - x)] * pattern[y, x]
            output[i - 1][j - 1] = actual_sum
    return output.astype(int)


def do_scipy_convolve(matrix: np.array, pattern: np.array) -> np.array:
    for i in range(3):
        # mode=same pour éviter que la sortie soit plus grande que l'entrée
        matrix[:, :, i] = convolve2d(matrix[:, :, i], pattern, mode="same")
    return matrix.astype(np.uint8)


def do_exercise1():
    array = np.array([[2, 1, 3, 0], [1, 1, 0, 5], [3, 3, 1, 0], [2, 0, 0, 2]])
    pattern = np.array([[1, 0, 2], [2, 1, 0], [1, 0, 3]])
    print(
        f"array: \n {array}\n pattern: \n{pattern}\n convolution: \n{do_convolution(array, pattern)}"
    )


def do_exercise2():
    array = np.array([[2, 1, 3, 0], [1, 1, 0, 5], [3, 3, 1, 0], [2, 0, 0, 2]])
    pattern = np.array([[1, 0, 2], [2, 1, 0], [1, 0, 3]])
    print(
        f"array: \n {array}\n pattern: \n{pattern}\n Scipy convolution: \n{convolve2d(array, pattern, mode='same')}"
    )


def do_exercise3(pattern_size):
    image = Image.open("./images/chat-vert.jpg")
    array = do_scipy_convolve(
        np.array(image),
        np.ones((pattern_size, pattern_size)) / (pattern_size**2),
    )

    Image.fromarray(array).save("./output/ex3_blur.jpeg")


def do_exercise4():
    image = Image.open("./images/chat-vert.jpg")
    array = do_scipy_convolve(
        np.array(image), np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]]) / 16
    )
    Image.fromarray(array).save("./output/ex4_gaussian_blur.jpeg")


if __name__ == "__main__":
    # do_exercise1()
    # do_exercise2()
    do_exercise3(10)
    do_exercise4()
