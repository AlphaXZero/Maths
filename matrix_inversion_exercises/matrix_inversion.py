import random
import math
import numpy as np
from typing import TypeAlias

Matrix: TypeAlias = list[list[float]]
Rowcol: TypeAlias = tuple[int, int]


def create_random_matrix(rowcol: Rowcol) -> Matrix:
    return [[random.randint(0, 10) for _ in range(rowcol[1])] for _ in range(rowcol[0])]


def swap_row(matrix: Matrix, row1: int, row2: int) -> Matrix:
    matrix[row1], matrix[row2] = matrix[row2], matrix[row1]
    return matrix


def subtract_row(matrix: Matrix, row1: int, row2: int, k: int) -> Matrix:
    matrix[row1] = [i - j * k for i, j in zip(matrix[row1], matrix[row2])]
    return matrix


def divide_row(matrix: Matrix, row: int, k: int) -> Matrix:
    matrix[row] = list(map(lambda x: x / k, matrix[row]))
    return matrix


def get_determinant_by_gauss(matrix: Matrix) -> float:
    # TODO déterminatn quand 0 ??
    for i, row in enumerate(matrix):
        if row[i] == 0:
            return 0
        for j in range(i + 1, len(matrix)):
            k = matrix[j][i] / matrix[i][i]
            matrix = subtract_row(matrix, j, i, k)
    return math.prod([matrix[i][i] for i in range(len(matrix))])


def get_identity_matrix(matrix: Matrix) -> Matrix:
    return [
        [1 if i == j else 0 for j in range(len(row))] for i, row in enumerate(matrix)
    ]


def do_gauss_forward_elimination(matrix: Matrix, inv_matrix: Matrix) -> tuple[Matrix]:
    """
    Take the max value in each row's first column, then swap rows if the max is not in the first row (to avoid division by zero).
    Divide the first row to get a 1 in the first column, then subtract this row from every other row with a coefficient if needed.
    Repeat, starting with the second row and second column, and so on.
    return a tuple with the matrix that will became the unit matrix and the inverted_matrix
    """
    for actual_index in range(len(matrix) - 1):
        pivot_row = [
            i
            for i in matrix
            if i[actual_index] == max([i[actual_index] for i in matrix])
        ][0]
        if matrix.index(pivot_row) != actual_index:
            inv_matrix = swap_row(inv_matrix, matrix.index(pivot_row), actual_index)
            matrix = swap_row(matrix, matrix.index(pivot_row), actual_index)
        inv_matrix = divide_row(inv_matrix, actual_index, pivot_row[actual_index])
        matrix = divide_row(matrix, actual_index, pivot_row[actual_index])
        for i in range(actual_index + 1, len(matrix)):
            inv_matrix = subtract_row(
                inv_matrix, i, actual_index, matrix[i][actual_index]
            )
            matrix = subtract_row(matrix, i, actual_index, matrix[i][actual_index])
    inv_matrix = divide_row(inv_matrix, -1, matrix[-1][-1])
    matrix = divide_row(matrix, -1, matrix[-1][-1])
    return matrix, inv_matrix


def do_gauss_backward_elimination(matrix: Matrix, inv_matrix: Matrix) -> Matrix:
    """
    Start from the last column of the penultimate row (because it is the value we want to eliminate),
    then eliminate that value using the row corresponding to the current column.
    return a tuple with the matrix that became the unit matrix and the inverted_matrix
    """
    for i in range(len(matrix) - 2, -1, -1):
        for j in range(i + 1, len(matrix)):
            if matrix[i][j] != 0:
                inv_matrix = subtract_row(inv_matrix, i, j, matrix[i][j])
                matrix = subtract_row(matrix, i, j, matrix[i][j])
    return matrix, inv_matrix


def do_gauss_jordan_inversion(matrix: Matrix) -> Matrix | None:
    if get_determinant_by_gauss([row[:] for row in matrix]) == 0:
        print("Matrix can't be inverted because the determinant is zero")
        return [[]]
    inv_matrix = get_identity_matrix(matrix)
    matrix, inv_matrix = do_gauss_backward_elimination(
        *do_gauss_forward_elimination(matrix, inv_matrix)
    )
    return [[round(x, 2) for x in row] for row in inv_matrix]


def format_equation_solution(reverted_matrix: Matrix, solution_matrix: Matrix) -> None:
    for i, row in enumerate(reverted_matrix):
        print(row, end="")
        print(solution_matrix[i])


def system_of_equations_solver() -> Matrix:
    matrix, solutions = ask_system_of_equations()
    if get_determinant_by_gauss([row[:] for row in matrix]) == 0:
        print("Matrix can't be inverted because the determinant is zero")
    matrix, solutions = do_gauss_backward_elimination(
        *do_gauss_forward_elimination(matrix, solutions)
    )
    return format_equation_solution(
        matrix, [[round(x, 2) for x in row] for row in solutions]
    )


def ask_system_of_equations() -> Matrix:
    nbr_unknows = int(input("How many unknows ? "))
    nbr_equations = int(input("How many equations ? "))
    if nbr_unknows != nbr_equations:
        print(
            "Cannot solve the system using Gauss: number of equations must equal number of unknowns."
        )
        return None
    unknow_list = [[0 for _ in range(nbr_unknows)] for row in range(nbr_unknows)]
    solutions_list = [[0] for _ in range(nbr_equations)]
    for i in range(nbr_unknows):
        for j in range(nbr_unknows + 1):
            while True:
                try:
                    nbr = int(input(f"Enter the value for m{i + 1}{j + 1}: "))
                    if j < nbr_unknows:
                        unknow_list[i][j] = int(nbr)
                    else:
                        solutions_list[i][0] = int(nbr)
                    break
                except ValueError:
                    print("incorect value, please retry")
    return unknow_list, solutions_list


def printm(matrix: Matrix) -> None:
    for i in matrix:
        print(i)


def test_ex1():
    A = create_random_matrix((4, 4))
    print("random matrix", A)
    A = swap_row(A, 0, 1)
    print("matrix with row 1 and 2 inverted", A)


def test_ex2():
    A = create_random_matrix((4, 4))
    print("random matrix", A)
    A = subtract_row(A, 0, 1, 2)
    print("maatrix with row 1 - (2 * row 2)", A)


def test_ex3():
    A = create_random_matrix((4, 4))
    print("random matrix", A)
    print("w/ np", np.linalg.det(A))
    print("w/o np", get_determinant_by_gauss(A))


def test_ex4():
    wiki_matrix = [[2, -1, 0], [-1, 2, -1], [0, -1, 2]]
    course_matrix = [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
    zero_det_matrix = [[1, 3, 3, 1], [1, 4, 3, 0], [1, 3, 4, 2], [2, 1, 0, 1]]
    labels = [
        "matrix " + i for i in ["from wiki", "from course", "with zero determinant"]
    ]
    for label, matrix in zip(labels, [wiki_matrix, course_matrix, zero_det_matrix]):
        print(f"{label} before inversion: ")
        printm(matrix)
        print(f"{label} after inversion:")
        printm(do_gauss_jordan_inversion(matrix))
        print("-----------------------------")


if __name__ == "__main__":
    # test_ex1()
    # test_ex2()
    # test_ex3()
    # test_ex4()
    print(system_of_equations_solver())
