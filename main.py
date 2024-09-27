import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import functions
from scipy.signal import find_peaks

# Загружаем изображения
im = cv.imread('image1.png')
sh = cv.imread('shum1.png')

# Преобразуем в градации серого для корректного анализа
gray_im = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
gray_sh = cv.cvtColor(sh, cv.COLOR_BGR2GRAY)

# Преобразуем изображения в 16-битные для корректного вычитания
gray_im = gray_im.astype(np.int16)
gray_sh = gray_sh.astype(np.int16)

# Получаем размеры изображения
vys, shir = gray_im.shape

# Инициализируем массивы для интенсивностей
dirt = functions.intensdirt_calc(gray_im)
clean = functions.intensclean_calc(gray_im, gray_sh)

# Параметры сглаживания
window_size = 10
clean_smooth = functions.moving_average(clean, window_size)
dirt_smooth = functions.moving_average(dirt, window_size)

# Нормализация интенсивности
clean_smooth = clean_smooth / np.max(clean_smooth)
dirt_smooth = dirt_smooth / np.max(dirt_smooth)
clean_smooth[320] = clean_smooth[320] - 0.005

# Поиск максимумов и минимумов с использованием библиотеки find_peaks
maximumy, _ = find_peaks(clean_smooth, distance=30)
minimumy, _ = find_peaks(-clean_smooth, distance=10)

# Исключаем крайние максимумы
maximumy = maximumy[1:-1]
minimumy = minimumy[1: ]

# Рассчитываем видимость
visibility_dirt, x_visibility = functions.visability_calc(dirt_smooth, minimumy, maximumy)
visibility_clean, _ = functions.visability_calc(clean_smooth, minimumy, maximumy)

# Добавляем крайние точки для видимости и координат
x_visibility = np.array([0] + x_visibility + [shir])*4.5
visibility_dirt = [0] + visibility_dirt + [0]
visibility_clean = [0] + visibility_clean + [0]


# Построение графика интенсивности после сглаживания
plt.figure(figsize=(10, 6))
x_values = np.arange(shir)*4.5
plt.plot(x_values, clean_smooth, color='green', label='после удаления шума (сглаживание)')
plt.scatter(maximumy*4.5, clean_smooth[maximumy], color='red', label='Максимумы', zorder=5)
plt.scatter(minimumy*4.5, clean_smooth[minimumy], color='blue', label='Минимумы', zorder=5)
plt.xlabel('Координата х в микронах')
plt.ylabel('Интенсивность')
plt.title('Зависимость интенсивности от координаты')
plt.legend()
plt.grid(True)
plt.xlim(0, shir*4.5)
plt.show()

# Построение графика сглаженной видимости с помощью кубического сплайна
# x_cubed, y_cubed = functions.cubic_splain(x_visibility, visibility)

plt.figure(figsize=(10, 6))
# plt.plot(x_visibility, visibility_dirt, color='red')
# plt.scatter(x_visibility, visibility_dirt, color='red', label='До удаления шума')
plt.plot(x_visibility, visibility_clean, color = 'green')
plt.scatter(x_visibility, visibility_clean, color = 'green', label='После удаления шума')
plt.xlabel('Координата в микронах')
plt.ylabel('видность (V)')
plt.title('Видность после удаления шума (источник далеко, нормировка интенсивности произведена)')
plt.grid(True)
plt.legend()
plt.xlim(0, shir*4.5)
plt.show()

# Повторяем процесс для другого изображения
im = cv.imread('image4.png')
gray_im = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
gray_im = gray_im.astype(np.int16)
vys, shir = gray_im.shape

# Интенсивность грязи
dirt = functions.intensdirt_calc(gray_im)
dirt = dirt / max(dirt)

# Поиск максимумов и минимумов
maximumy, _ = find_peaks(dirt, distance=15)
minimumy, _ = find_peaks(-dirt, distance=15)
maximumy = maximumy[2:-2]

# Рассчет видимости
visibility, x_visibility = functions.visability_calc(dirt, minimumy, maximumy)

# Построение графика интенсивности грязи
plt.figure(figsize=(10, 6))
plt.plot(np.arange(shir), dirt, color='green', label='после удаления шума (сглаживание)')
plt.scatter(maximumy, dirt[maximumy], color='red', label='Максимумы', zorder=5)
plt.scatter(minimumy, dirt[minimumy], color='blue', label='Минимумы', zorder=5)
plt.xlabel('Координата х в пикселях')
plt.ylabel('Интенсивность')
plt.title('Зависимость интенсивности от координаты')
plt.legend()
plt.grid(True)
plt.xlim(0, shir)
plt.show()

# Построение графика сглаженной видимости для второго изображения
x_visibility = [0] + x_visibility + [shir]
visibility = [0] + visibility + [0]

plt.figure(figsize=(10, 6))
plt.plot(x_visibility, visibility, color='purple', label='видность')
plt.scatter(x_visibility, visibility, color='orange', label='Исходные точки видности')
plt.xlabel('Средняя координата между максимумом и минимумом (пиксели)')
plt.ylabel('Видность (V)')
plt.title('Зависимость видности от координаты x')
plt.grid(True)
plt.legend()
plt.xlim(0, shir)
plt.show()