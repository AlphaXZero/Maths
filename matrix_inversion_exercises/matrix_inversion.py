import random
import math
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
    for i in range(len(matrix) - 1):
        for j in range(len(matrix) - i - 1):
            k = (
                matrix[i + 1 + j][0 + i] / matrix[i][0 + i]
                if matrix[i][0 + i] != 0
                else 1
            )
            matrix = substract_row(matrix, i + 1 + j, i, k)
    return math.prod([matrix[i][i] for i in range(len(matrix))])


def gauss_jordan(matrix: Matrix):
    for i in range(len(matrix[0])):
        row_with_max = get_row_where_max_first_col(matrix)
        if row_with_max != 0:
            matrix = invert_row(matrix, 0, row_with_max)
            matrix = divide_row(matrix, 0, matrix[0][0])

    return matrix


def get_row_where_max_first_col(matrix: Matrix):
    maxi = -100000
    ind = 0
    for i, row in enumerate(matrix):
        if row[0] > maxi:
            maxi, ind = row[0], i
    return ind


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
    print("maatrix with row 1 - 2 * row 2", A)


def test_ex3():
    oui = [[1, 3, 3, 1], [1, 4, 3, 0], [1, 3, 4, 2], [2, 1, 0, 1]]
    A = create_random_matrix((4, 4))
    printm(oui)
    print("----------------------")
    oui = determinant_gaussian(oui)
    printm(oui)


if __name__ == "__main__":
    oui = [[1, 3, 3, 1], [1, 4, 3, 0], [1, 3, 4, 2], [2, 1, 0, 1]]
    print(gauss_jordan(oui))
