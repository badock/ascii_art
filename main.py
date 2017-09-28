import numpy as np
from scipy.interpolate import interp2d
import matplotlib.pyplot as plt
from PIL import Image

MINITEL_WIDTH = 40
MINITEL_HEIGHT = 25

if __name__ == "__main__":
    plt.ioff()

    # image_path = "img/rocket.png"
    image_path = "img/lena.png"
    # image_path = "img/vangogh.png"
    # image_path = "img/deathstar.png"
    # image_path = "img/screenshot.png"
    # image_path = "img/imtlogo.png"
    img = Image.open(image_path).convert("RGB")
    pixels = img.load()

    ascii_result = []
    for i in range(0, img.height):
        current_line = []
        for j in range(0, img.width):
            current_pixel = pixels[j,i]
            gray_value = float(current_pixel[0]) / 3 + float(current_pixel[1]) / 3 + float(current_pixel[2]) / 3
            gray_value = int(gray_value / float(255) * float(7))
            current_line += [gray_value]
        ascii_result += [current_line]

    x = np.linspace(0, img.width-1, img.width)
    y = np.linspace(0, img.height-1, img.height)
    X, Y = np.meshgrid(x, y)

    Z_old = np.sin(np.pi * X / 2) * np.exp(Y / 2)
    Z = np.array(ascii_result)

    x2 = np.linspace(0, img.width-1, MINITEL_WIDTH)
    y2 = np.linspace(0, img.height-1, MINITEL_HEIGHT)
    f = interp2d(x, y, Z, kind='cubic')
    Z2 = f(x2, y2)

    fig, ax = plt.subplots(nrows=1, ncols=4)
    ax[0].pcolormesh(X, Y, Z)

    X2, Y2 = np.meshgrid(x2, y2)
    ax[1].pcolormesh(X2, Y2, Z2)

    # Third image
    x3 = np.linspace(0, img.width - 1, MINITEL_WIDTH * 2)
    y3 = np.linspace(0, img.height - 1, MINITEL_HEIGHT * 3)
    f = interp2d(x, y, Z, kind='cubic')
    Z3 = f(x3, y3)

    X3, Y3 = np.meshgrid(x3, y3)
    ax[2].pcolormesh(X3, Y3, Z3)

    # Fourth image
    ascii_art_result = []
    for i in range(0, MINITEL_HEIGHT):
        current_line_1 = []
        current_line_2 = []
        current_line_3 = []
        for j in range(0, MINITEL_WIDTH):
            x = i * 3
            y = j * 2
            current_pixel_subpixels = [Z3[x, y], Z3[x+1, y], Z3[x+2, y], Z3[x, y+1], Z3[x+1, y+1], Z3[x+2, y+1]]
            average_pixel_value = np.mean(current_pixel_subpixels)
            current_pixel_pseudopixels_values = map(lambda x: 1 if x >= average_pixel_value else 0, current_pixel_subpixels)
            displayed_values = filter(lambda x: x >= average_pixel_value, current_pixel_subpixels)
            background_values = filter(lambda x: x < average_pixel_value, current_pixel_subpixels)
            displayed_values_mean = np.mean(displayed_values)
            background_values_mean = np.mean(background_values)

            current_pixel_pseudopixels_values_np = map(lambda x: displayed_values_mean if x == 1 else background_values_mean, current_pixel_pseudopixels_values)

            byte = 0
            current_line_1 += [current_pixel_pseudopixels_values_np[0], current_pixel_pseudopixels_values_np[3]]
            current_line_2 += [current_pixel_pseudopixels_values_np[1], current_pixel_pseudopixels_values_np[4]]
            current_line_3 += [current_pixel_pseudopixels_values_np[2], current_pixel_pseudopixels_values_np[5]]
        ascii_art_result += [current_line_1]
        ascii_art_result += [current_line_2]
        ascii_art_result += [current_line_3]

    x4 = np.linspace(0, img.width - 1, MINITEL_WIDTH * 2)
    y4 = np.linspace(0, img.height - 1, MINITEL_HEIGHT * 3)
    Z4 = np.array(ascii_art_result)

    X4, Y4 = np.meshgrid(x4, y4)
    ax[3].pcolormesh(X4, Y4, Z4)

    ax[0].invert_yaxis()
    ax[1].invert_yaxis()
    ax[2].invert_yaxis()
    ax[3].invert_yaxis()

    plt.show()
