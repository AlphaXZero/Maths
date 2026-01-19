import numpy as np


def do_convolution(matrix: np.ndarray, pattern: np.ndarray):
    output = np.zeros(matrix.shape)
    matrix = np.insert(matrix, 0, np.zeros((matrix.shape[1])), axis=0)
    matrix = np.insert(matrix, 0, np.zeros((matrix.shape[0])), axis=1)
    matrix = np.insert(matrix, matrix.shape[0], np.zeros((matrix.shape[1])), axis=0)
    matrix = np.insert(matrix, matrix.shape[1], np.zeros((matrix.shape[0])), axis=1)
    print(matrix)
    for i in range(1, matrix.shape[0] - 1):
        for j in range(1, matrix.shape[1] - 1):
            actual_sum = 0
            for y in range(pattern.shape[0]):
                for x in range(pattern.shape[1]):
                    actual_sum += matrix[i - (1 - y), j - (1 - x)] * pattern[y, x]
            output[i - 1][j - 1] = actual_sum
    return output
