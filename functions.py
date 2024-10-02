import numpy as np
from scipy.interpolate import CubicSpline
import cairosvg
import cv2


def svg_to_png(image):
    cairosvg.svg2png(url=image, write_to='image.png')
    image2 = cv2.imread('image.png')
    return image2

# Функция для расчета интенсивности "грязи"
def intensdirt_calc(gray_im):
    vys, shir = gray_im.shape
    return np.sum(gray_im, axis=0)  # Суммируем по оси y для каждого x

# Функция для расчета интенсивности "чистоты"
def intensclean_calc(gray_im, sh):
    vys, shir = gray_im.shape
    a = np.zeros(shir)

    for x in range(shir):
        a[x] = np.sum([(gray_im[y, x]) - (sh[y, x]) for y in range(vys)])
    return a

# Функция для расчета скользящего среднего
def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size) / window_size, mode='same')

# Функция для расчета видимости на основе максимумов и минимумов
def visability_calc(clean_smooth, minimumy, maximumy):
    min_len = min(len(maximumy), len(minimumy))
    visibility, x_visibility = [], []

    i_max, i_min = 0, 0
    while i_max < len(maximumy) and i_min < len(minimumy):
        I_max = clean_smooth[maximumy[i_max]]
        I_min = clean_smooth[minimumy[i_min]]

        # Рассчитываем видимость
        V = (I_max - I_min) / (I_max + I_min) if (I_max + I_min) != 0 else 0
        visibility.append(V)

        # Средняя координата между максимумом и минимумом
        mid_x = (maximumy[i_max] + minimumy[i_min]) / 2
        x_visibility.append(mid_x)

        # print(f'Imax = {I_max}, Imin = {I_min}, V = {V}')

        # Обновляем индексы
        if minimumy[i_min] < maximumy[i_max]:
            i_min += 1
        else:
            i_max += 1

    return visibility, x_visibility

# Функция для построения кубического сплайна
def cubic_splain(x_visibility, visibility):
    cs = CubicSpline(x_visibility, visibility)
    x_new = np.linspace(min(x_visibility), max(x_visibility), 1000)
    y_new = cs(x_new)
    return x_new, y_new

# Функция для интегрирования значений для нормировки (не используется в main)
def intgr_for_normir(im):
    return np.sum(functions.intensdirtf(im))


def polynomial_interpolation(x_visibility, visibility, degree=5):
    # Подбираем полином степени degree через метод наименьших квадратов
    coefficients = np.polyfit(x_visibility, visibility, degree)

    # Создаем полиномиальную функцию
    poly_func = np.poly1d(coefficients)

    # Генерируем новые точки для более плавного графика
    x_new = np.linspace(min(x_visibility), max(x_visibility), 1000)
    y_new = poly_func(x_new)

    return x_new, y_new
