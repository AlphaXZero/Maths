from PIL import Image
import numpy as np
from scipy.signal import convolve2d


def do_exercise_1():
    image = Image.open("./images/chat-vert.jpg")
    array = np.array(image)
    nb_lignes, nb_colonnes, _ = array.shape
    print(f"lignes : {nb_lignes}, colonnes : {nb_colonnes}")
    Image.fromarray(array).save("./output/ex1_copy.jpeg")


def do_exercise_2():
    image = Image.open("./images/6x2.png")
    array = np.array(image)
    print(array)
    print(array[0, 1])


def do_exercise_3():
    image = Image.open("./images/chat-vert.jpg")
    array = np.array(image)
    Image.fromarray(array[0 : (array.shape[0] // 2), 0 : array.shape[1]]).save(
        "./output/ex3_cut.jpeg"
    )


def do_exercise_4():
    image = Image.open("./images/chat-vert.jpg")
    array = np.array(image)
    Image.fromarray(np.array([i[::-1] for i in array])).save("./output/ex4_hflip.jpeg")
    Image.fromarray(np.array([i for i in array[::-1]])).save("./output/ex4_vflip.jpeg")


def do_exercise_5():
    image = Image.open("./images/chat-vert.jpg")
    array = np.array(image)
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            array[i][j] = [
                255 - array[i][j][0],
                255 - array[i][j][1],
                255 - array[i][j][2],
            ]
    Image.fromarray(array).save("./output/ex5_negative.jpeg")


def do_exercise_6():
    image = Image.open("./images/4-2-03.jpg")
    array = np.array(image)
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            array[i][j] = [array[i][j][1], 0, 0]
    Image.fromarray(array).save("./output/ex6_isolate_red.jpeg")


def do_exercise_6_2():
    image = Image.open("./images/4-2-03.jpg")
    array = np.array(image)
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            r, g, b = array[i][j]
            if not (
                abs(int(r) - int(g)) < 40 and b < 100 and 40 < r < 200 and 40 < g < 200
            ):
                array[i][j] = [0, 0, 0]
    Image.fromarray(array).save("./output/ex6_2_isolate_yellow.jpg")


def do_exercise_7():
    image = Image.open("./images/chat-vert.jpg")
    array = np.array(image)
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            lum = (
                int(array[i][j][0] * 0.2126)
                + int(array[i][j][1] * 0.7152)
                + int(array[i][j][2] * 0.0722)
            )
            array[i][j] = [lum, lum, lum]
    Image.fromarray(array).save("./output/ex7_grey_transformation.jpeg")


def do_exercise_8(light_ammount: int):
    def add_light(x):
        return min(int(x) + light_ammount, 255)

    image = Image.open("./images/chat-vert.jpg")
    array = np.array(image)
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            array[i][j] = [
                add_light(array[i][j][0]),
                add_light(array[i][j][1]),
                add_light(array[i][j][2]),
            ]
    Image.fromarray(array).save("./output/ex8_lighten.jpeg")


def do_exercise_9(percentage_first_image: int):
    percentage_second_image = 100 - percentage_first_image

    def add_light(a, b):
        return min(
            int(a) * percentage_first_image / 100
            + int(b) * percentage_second_image / 100,
            255,
        )

    image1 = Image.open("./images/chat-vert.jpg")
    image2 = Image.open("./images/fond-pour-chat-vert.jpg")
    array1 = np.array(image1)
    array2 = np.array(image2)
    for i in range(array1.shape[0]):
        for j in range(array2.shape[1]):
            array1[i][j] = [
                add_light(array1[i][j][0], array2[i][j][0]),
                add_light(array1[i][j][1], array2[i][j][0]),
                add_light(array1[i][j][2], array2[i][j][0]),
            ]
    Image.fromarray(array1).save("./output/ex9_combine_images.jpeg")


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


if __name__ == "__main__":
    # do_exercise_1()
    # do_exercise_2()
    # do_exercise_3()
    # do_exercise_4()
    # do_exercise_5()
    # do_exercise_6()
    # do_exercise_6_2()
    # do_exercise_7()
    # do_exercise_8(120)
    do_exercise_9(40)
