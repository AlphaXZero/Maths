from PIL import Image
import numpy as np
from math import prod


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

    def combine_pixels(a, b):
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
                combine_pixels(array1[i][j][0], array2[i][j][0]),
                combine_pixels(array1[i][j][1], array2[i][j][1]),
                combine_pixels(array1[i][j][2], array2[i][j][2]),
            ]
    Image.fromarray(array1).save("./output/ex9_combine_images.jpeg")


def do_exercise_10():
    image1 = Image.open("./images/chat-vert.jpg")
    image2 = Image.open("./images/fond-pour-chat-vert.jpg")

    array1 = np.array(image1)
    array2 = np.array(image2)
    for i in range(array1.shape[0]):
        for j in range(array2.shape[1]):
            array1[i][j] = array1[i][j] if array1[i][j][1] != 255 else array2[i][j]
    Image.fromarray(array1).save("./output/ex10_green_background.jpeg")


def do_exercise_11():
    def get_average_pixels(cell):
        return sum(cell) // 3

    image = Image.open("./images/fond-pour-chat-vert.jpg")
    array = np.array(image).astype(dtype=int)
    array_flatten = array.reshape(prod(array.shape[0:2]), 3)
    i_min = min((map(get_average_pixels, array_flatten)))
    i_max = max((map(get_average_pixels, array_flatten)))

    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            r, g, b = array[i, j]
            if i_max == i_min:
                pass
            array[i, j] = (
                min(max(int(255 * (r - i_min) / (i_max - i_min)), 0), 255),
                min(max(int(255 * (g - i_min) / (i_max - i_min)), 0), 255),
                min(max(int(255 * (b - i_min) / (i_max - i_min)), 0), 255),
            )
    array = array.astype(dtype=np.uint8)
    Image.fromarray(array).save("./output/ex11_change_constrast.jpeg")


def do_exercise_12(size: tuple[int]):
    image = Image.open("./images/chat-vert.jpg")
    array = np.array(image)
    array2 = np.zeros((size[0], size[1], 3))
    ratio = array.shape[0] / size[0], array.shape[1] / size[1]

    for i in range(array2.shape[0]):
        for j in range(array2.shape[1]):
            array2[i][j] = array[int(i * ratio[0]), int(j * ratio[1])]
    array2 = array2.astype(dtype=np.uint8)
    Image.fromarray(array2).save("./output/ex12_resize.jpg")


def do_exercise_13():
    # TODO : que faire ?
    return None


def test_grey_conversion():
    # TODO comment faire ?
    image = Image.open("./images/chat-vert.jpg")
    array = np.array(image)
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            gray = min(255, sum((array[i][j][0], array[i][j][1], array[i][j][2])) // 3)
            array[i][j] = gray
    Image.fromarray(array.astype(np.uint8)).save("./output/grey_test.jpeg")


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
    # do_exercise_9(40)
    # do_exercise_10()
    # do_exercise_11()
    # do_exercise_12((900, 900))
    # do_exercise_13()
    test_grey_conversion()
