import re

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os

height = 224
width = 224


def mix_photos(photos, mix_ratio):
    files_count = 2
    filename = './static/result.jpg'
    image_box = [[]] * files_count
    images_resized = [[]] * files_count
    for file_i in range(files_count):
        #открываем изображение
        image_box[file_i] = Image.open(photos[file_i])
        #изменяем размер, приводим значения rgb к диапазону от 0 до 1
        images_resized[file_i] = np.array(image_box[file_i].resize((height, width)))/255.0

    images_resized = np.array(images_resized)
    #Попиксильное смешивание двух изображений
    image_ = images_resized[0] * mix_ratio + images_resized[1] * (1-mix_ratio)
    image_result = Image.fromarray((image_ * 255).astype(np.uint8))
    image_result.save(filename)
    return filename


def gist_colors(filename):
    print(f'файл название {filename}')
    image = Image.open(filename)
    #Выделяем имя файла из пути
    result_name = os.path.basename(filename)
    #Записываем полный путь до будущей диаграммы. Для каждого файла создаётся уникальный файл диаграммы
    full_result_path = f'./static/{result_name}_gist.jpg'
    image = np.array(image.resize((height, width)))
    colors_value = [0] * 3
    colors_name = ['red', 'green', 'blue']
    #Расчёт среднего значения по всем пикселям
    for line in image:
        for pixel in line:
            for color in range(3):
                colors_value[color] += pixel[color]
    for color in range(3):
        colors_value[color] /= 224*224
    print(colors_value, colors_name)
    #Построение диаграммы
    fig, axes = plt.subplots()
    axes.bar(colors_name, colors_value)
    axes.set_title(result_name)
    plt.savefig(full_result_path)
    return full_result_path
