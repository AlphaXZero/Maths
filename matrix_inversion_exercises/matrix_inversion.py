import random
import math
import numpy as np
from typing import TypeAlias

global operations
operations = []

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
    # TODO déterminatn quand 0 ??
    for i, row in enumerate(matrix):
        if row[i] == 0:
            return 0
        for j in range(i + 1, len(matrix)):
            k = matrix[j][i] / matrix[i][i]
            matrix = substract_row(matrix, j, i, k)
    return math.prod([matrix[i][i] for i in range(len(matrix))])


def identity_matrix(matrix: Matrix) -> Matrix:
    return [
        [1 if i == j else 0 for j in range(len(row))] for i, row in enumerate(matrix)
    ]


def gauss_jordan_lower_triangular(matrix: Matrix, output: Matrix) -> tuple[Matrix]:
    """
    Take the max value in each row's first column, then switch rows if the max is not in the first row (to avoid division by zero).
    Divide the first row to get a 1 in the first column, then subtract this row from every other row with a coefficient if needed.
    Repeat, starting with the second row and second column, and so on.
    """
    for actual_index in range(len(matrix) - 1):
        line_where_max = [
            i
            for i in matrix
            if i[actual_index] == max([i[actual_index] for i in matrix])
        ][0]
        if matrix.index(line_where_max) != actual_index:
            matrix = invert_row(matrix, matrix.index(line_where_max), actual_index)
            output = invert_row(output, matrix.index(line_where_max), actual_index)
        output = divide_row(output, actual_index, line_where_max[actual_index])
        matrix = divide_row(matrix, actual_index, line_where_max[actual_index])
        for i in range(actual_index + 1, len(matrix)):
            output = substract_row(output, i, actual_index, matrix[i][actual_index])
            matrix = substract_row(matrix, i, actual_index, matrix[i][actual_index])
    output = divide_row(output, -1, matrix[-1][-1] if matrix[-1][-1] != 0 else 1)
    matrix = divide_row(matrix, -1, matrix[-1][-1] if matrix[-1][-1] != 0 else 1)
    return matrix, output


def gauss_jordan_upper_triangular(matrix: Matrix, output: Matrix) -> Matrix:
    """
    Start from the last column of the penultimate row (because it is the value we want to eliminate),
    then eliminate that value using the row corresponding to the current column.
    """
    for i in range(len(matrix) - 2, -1, -1):
        for j in range(i + 1, len(matrix)):
            if matrix[i][j] != 0:
                output = substract_row(output, i, j, matrix[i][j])
                matrix = substract_row(matrix, i, j, matrix[i][j])
    return matrix, output


def gauss_jordan_inversion_matrix(matrix: Matrix) -> Matrix:
    output = identity_matrix(matrix)
    matrix, output = gauss_jordan_upper_triangular(
        *gauss_jordan_lower_triangular(matrix, output)
    )
    printm(matrix)
    return [[round(x, 2) for x in row] for row in output]


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
    # test_ex1()
    # test_ex2()
    # test_ex3()
    oui = [[1, 3, 3, 1], [1, 4, 3, 0], [1, 3, 4, 2], [2, 1, 0, 1]]
    oui2 = [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
    test_wiki = [[2, -1, 0], [-1, 2, -1], [0, -1, 2]]
    printm(gauss_jordan_inversion_matrix(test_wiki))
    # print(operation)
