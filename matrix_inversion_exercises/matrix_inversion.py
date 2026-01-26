import random
import math
import numpy as np
from typing import TypeAlias

Matrix: TypeAlias = list[list[int]]
Rowcol: TypeAlias = tuple[int, int]


def create_random_matrix(rowcol: Rowcol) -> Matrix:
    return [[random.randint(0, 10) for _ in range(rowcol[1])] for _ in range(rowcol[0])]


def invert_row(matrix: Matrix, row1: int, row2: int) -> Matrix:
    matrix[row1], matrix[row2] = matrix[row2], matrix[row1]
    return matrix


def substract_row(matrix: Matrix, row1: int, row2: int, k: int) -> Matrix:
    matrix[row1] = [i - j * k for i, j in zip(matrix[row1], matrix[row2])]
    return matrix


def divide_row(matrix: Matrix, row: int, k: int) -> Matrix:
    matrix[row] = list(map(lambda x: x / k, matrix[row]))
    return matrix


def determinant_gaussian(matrix: Matrix) -> float:
    # TODO déterminatn quan 0
    for i, row in enumerate(matrix):
        if row[i] == 0:
            return 0
        for j in range(i + 1, len(matrix)):
            k = matrix[j][i] / matrix[i][i]
            matrix = substract_row(matrix, j, i, k)
    return math.prod([matrix[i][i] for i in range(len(matrix))])


def gauss_jordan(matrix: Matrix):
    for padding in range(len(matrix[0]) - 1):
        row_with_max = get_row_where_max_first_col(
            [a[padding:] for a in matrix[padding:]], padding
        )
        print(row_with_max)
        printm(matrix)
        print("----------------")

        if row_with_max != padding:
            matrix = invert_row(matrix, padding, row_with_max)
        matrix = divide_row(matrix, padding, matrix[padding][padding])
        for i in range(1, len(matrix)):
            matrix[i] = [
                matrix[i][j] - matrix[padding][j] for j in range(len(matrix[0]))
            ]

    return matrix


def get_row_where_max_first_col(matrix: Matrix, target: int):
    maxi = -100000
    ind = 0
    for i, row in enumerate(matrix):
        if row[0] > maxi:
            maxi, ind = row[i], i
    return ind + target


def printm(matrix: Matrix) -> None:
    for i in matrix:
        print(i)


def test_ex1():
    A = create_random_matrix((4, 4))
    print("random matrix", A)
    A = invert_row(A, 0, 1)
    print("matrix with row 1 and 2 inverted", A)


def test_ex2():
    A = create_random_matrix((4, 4))
    print("random matrix", A)
    A = substract_row(A, 0, 1, 2)
    print("maatrix with row 1 - (2 * row 2)", A)


def test_ex3():
    A = create_random_matrix((4, 4))
    print("random matrix", A)
    print("w/ np", np.linalg.det(A))
    print("w/o np", determinant_gaussian(A))


if __name__ == "__main__":
    oui = [[1, 3, 3, 1], [1, 4, 3, 0], [1, 3, 4, 2], [2, 1, 0, 1]]
    oui2 = [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
    # print(gauss_jordan(oui))
    test_ex3()
