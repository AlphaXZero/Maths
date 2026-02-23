from PIL import Image
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def hide_image(main_image, secret_image, output_image):
    """
    Hides secret_image inside main_image
    and saves the result to output_image
    """
    main_image = Image.open(main_image)
    secret_image = Image.open(secret_image)

    main_pixels = np.array(main_image)
    secret_pixels = np.array(secret_image)

    mx, my = main_image.size
    sx, sy = secret_image.size
    x, y = min(mx, sx), min(my, sy)
    for i in range(y):
        for j in range(x):
            main_pixels[i][j] = (
                (main_pixels[i, j][0] - (main_pixels[i, j][0] % 16))
                + secret_pixels[i, j][0] % 16,
                (main_pixels[i, j][1] - (main_pixels[i, j][1] % 16))
                + secret_pixels[i, j][1] % 16,
                (main_pixels[i, j][2] - (main_pixels[i, j][2] % 16))
                + secret_pixels[i, j][2] % 16,
                main_pixels[i, j][3],
            )

    Image.fromarray(main_pixels).save(output_image)


if __name__ == "__main__":
    hide_image(
        BASE_DIR / "images/main_image.png",
        BASE_DIR / "images/secret_image.png",
        BASE_DIR / "output/coded_image.png",
    )
