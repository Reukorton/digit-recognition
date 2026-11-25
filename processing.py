
import cv2
import numpy as np
from PIL import Image


def find_contours(image):
    # Преобразование изображения в массив
    image_array = np.array(image.convert("RGB"))

    # Перевод в оттенки серого
    gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)

    # Бинаризация изображения
    _, brightness_mask = cv2.threshold(
        gray, 127, 255, cv2.THRESH_BINARY_INV
    )

    red = image_array[:, :, 0].astype(np.int16)
    blue = image_array[:, :, 2].astype(np.int16)

    temperature = red - blue

    warm_mask = np.where(
        temperature > 30, 255, 0
    ).astype(np.uint8)

    binary = cv2.bitwise_or(
        brightness_mask, warm_mask
    )

    # Поиск контуров
    contours, _ = cv2.findContours(
        binary,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # Создание белого фона
    result = np.full_like(image_array, 255)

    # Отрисовка контуров красным цветом
    cv2.drawContours(
        result, contours, -1, (255, 0, 0), 2
    )

    return Image.fromarray(result)
