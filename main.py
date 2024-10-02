import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import functions
from scipy.signal import find_peaks

# Загружаем изображения
im_udal = cv.imread('image1.png')
sh_udal = cv.imread('shum1.png')
im_upor = cv.imread('image2.png')
sh_upor = cv.imread('shum2.png')

theor = cv.imread('theor.png')

# Преобразуем в градации серого для корректного анализа
gray_im_udal = cv.cvtColor(im_udal, cv.COLOR_BGR2GRAY)
gray_sh_udal = cv.cvtColor(sh_udal, cv.COLOR_BGR2GRAY)

gray_im_upor = cv.cvtColor(im_upor, cv.COLOR_BGR2GRAY)
gray_sh_upor = cv.cvtColor(sh_upor, cv.COLOR_BGR2GRAY)

gray_theor = cv.cvtColor(theor, cv.COLOR_BGR2GRAY)

# Преобразуем изображения в 16-битные для корректного вычитания
gray_im_udal = gray_im_udal.astype(np.int16)
gray_sh_udal = gray_sh_udal.astype(np.int16)

gray_im_upor = gray_im_upor.astype(np.int16)
gray_sh_upor = gray_sh_upor.astype(np.int16)

gray_theor = gray_theor.astype(np.int16)

# Получаем размеры изображения
vys_udal, shir_udal = gray_im_udal.shape
vys_upor, shir_upor = gray_im_upor.shape
vys_theor, shir_theor = gray_theor.shape

# Считаем массивы интенсивностей
dirt_upor = functions.intensdirt_calc(gray_im_upor)
dirt_udal = functions.intensdirt_calc(gray_im_udal)

clean_upor = functions.intensclean_calc(gray_im_upor, gray_sh_upor)
clean_udal = functions.intensclean_calc(gray_im_udal, gray_sh_udal)

theor_intens = functions.intensdirt_calc(gray_theor)

# Гладим
window_size = 10
clean_upor_smooth = functions.moving_average(clean_upor, window_size)
clean_udal_smooth = functions.moving_average(clean_udal, window_size)
dirt_upor_smooth = functions.moving_average(dirt_upor, window_size)
dirt_udal_smooth = functions.moving_average(dirt_udal, window_size)

theor_intens_smooth = functions.moving_average(theor_intens, 10)

# Обрезаем график теоретической интенсивности, чтобы сравнить нулевые порядки
theor_intens_smooth = theor_intens_smooth[int(shir_theor*0.26):int(shir_theor*0.76)]
theor_intens = theor_intens[int(shir_theor*0.26):int(shir_theor*0.76)]

# Поиск максимумов и минимумов с использованием библиотеки find_peaks
clean_udal_smooth[10] = clean_udal_smooth[10]*0.8
clean_udal_smooth[430] = clean_udal_smooth[430]*0.8

#Нормировка на интегральное
# clean_upor_smooth_n1 = clean_upor_smooth/6793489
# clean_udal_smooth_n1 = clean_udal_smooth/8013040
# theor_intens_smooth_n1 = theor_intens_smooth/1782183
# clean_upor_n1 = clean_upor/6793489
# clean_udal_n1 = clean_udal/8013040
# theor_intens_n1 = theor_intens/1782183

#Нормировка на максимальное
clean_upor_smooth_n2 = clean_upor_smooth/np.max(clean_upor_smooth)
clean_udal_smooth_n2 = clean_udal_smooth/np.max(clean_udal_smooth)
theor_intens_smooth_n2 = theor_intens_smooth/np.max(theor_intens_smooth)
clean_upor_n2 = clean_upor/np.max(clean_upor)
clean_udal_n2 = clean_udal/np.max(clean_udal)
theor_intens_n2 = theor_intens/np.max(theor_intens)

maximumy_udal, _ = find_peaks(clean_udal_smooth_n2, distance=30)
minimumy_udal, _ = find_peaks(-clean_udal_smooth_n2, distance=30)
maximumy_upor, _ = find_peaks(clean_upor_smooth_n2, distance =30)
minimumy_upor, _ = find_peaks(-clean_upor_smooth_n2, distance=30)

maximumy_theor, _ = find_peaks(theor_intens_smooth_n2, distance=10)
minimumy_theor, _ = find_peaks(-theor_intens_smooth_n2, distance=10)

#корректировка минмакса
maximumy_udal = maximumy_udal[1:-1]
minimumy_udal = minimumy_udal[:]
maximumy_upor = maximumy_upor[2:-2]
minimumy_upor = minimumy_upor[1:-1]

# Рассчитываем видность
visibility_upor_clean, x_visibility_upor_clean = functions.visability_calc(clean_upor_smooth_n2, minimumy_upor, maximumy_upor)
visibility_udal_clean, x_visibility_udal_clean = functions.visability_calc(clean_udal_smooth_n2, minimumy_udal, maximumy_udal)

visibility_theor, x_visibility_theor = functions.visability_calc(theor_intens_smooth, minimumy_theor, maximumy_theor)

# Добавляем крайние точки для видимости и координат
x_visibility_upor_clean = np.array(x_visibility_upor_clean)*(4.5*10**-3)
x_visibility_udal_clean = np.array(x_visibility_udal_clean)*(4.5*10**-3)

x_visibility_theor = np.array(x_visibility_theor)*(15.748*10**-3)

# Корректируем значения по Х для интенсивностей
x_values_udal = np.arange(shir_udal)*(4.5*10**-3)
x_values_upor = np.arange(shir_upor)*(4.5*10**-3)
x_values_theor = np.arange(shir_theor*0.5)*(15.748*10**-3)



# Графики интенсивностей
plt.figure(figsize=(10, 10))

plt.plot(x_values_upor, clean_upor_smooth_n2, color='green', label='после удаления шума (сглаживание, источник близко)')
plt.plot(x_values_udal, clean_udal_smooth_n2, color='purple', label='после удаления шума (сглаживание, источник поодаль)')
# plt.plot(x_values_upor, clean_upor_n2, color='yellow', label='после удаления шума (источник близко)')
plt.plot(x_values_theor, theor_intens_smooth_n2, color='red', label='теоретическая интенсивность (сглаживание)')
# plt.plot(x_values_theor, theor_intens_n2, color='blue', label='теоретическая интенсивность')
# plt.plot(x_values_upor, dirt_upor_smooth, color='orange', label='до удаления шума (сглаживание, источник близко)')
# plt.plot(x_values_udal, dirt_udal_smooth, color='purple', label='до удаления шума (сглаживание, источник поодаль)')

plt.scatter(maximumy_udal*(4.5*10**-3), clean_udal_smooth_n2[maximumy_udal], color='red', zorder=5)
plt.scatter(minimumy_udal*(4.5*10**-3), clean_udal_smooth_n2[minimumy_udal], color='yellow', zorder=5)
plt.scatter(maximumy_upor*(4.5*10**-3), clean_upor_smooth_n2[maximumy_upor], color='purple')
plt.scatter(minimumy_upor*(4.5*10**-3), clean_upor_smooth_n2[minimumy_upor], color='orange')
plt.scatter(minimumy_theor*(15.748*10**-3), theor_intens_smooth_n2[minimumy_theor], color='gray')
plt.scatter(maximumy_theor*(15.748*10**-3), theor_intens_smooth_n2[maximumy_theor], color='green')

plt.xlabel('Координата х в мм')
plt.ylabel('Интенсивность')
plt.title('Зависимость интенсивности от координаты (нормировка на максимальное значение)')
plt.legend()
plt.grid(True)
plt.show()

# Исследование интегрального значения
# im1 = cv.imread('UTK.png')
# im1 = cv.cvtColor(im1, cv.COLOR_BGR2GRAY)
# im1 = im1.astype(np.int16)
# sh1 = cv.imread('UTZ.png')
# sh1 = cv.cvtColor(sh1, cv.COLOR_BGR2GRAY)
# sh1 = sh1.astype(np.int16)
# intens1 = functions.intensclean_calc(im1, sh1)
#
# im2 = cv.imread('UPTK.png')
# im2 = cv.cvtColor(im2, cv.COLOR_BGR2GRAY)
# im2 = im2.astype(np.int16)
# sh2 = cv.imread('UPTZ.png')
# sh2 = cv.cvtColor(sh2, cv.COLOR_BGR2GRAY)
# sh2 = sh2.astype(np.int16)
# intens2 = functions.intensclean_calc(im2, sh2)
#
#
# print(np.sum(theor_intens), np.sum(intens1), np.sum(intens2))


x_visibility_upor_clean = np.insert(x_visibility_upor_clean, 0, 0)
x_visibility_udal_clean = np.insert(x_visibility_udal_clean, 0, 0)
x_visibility_udal_clean = np.append(x_visibility_udal_clean, 2)
x_visibility_upor_clean = np.append(x_visibility_upor_clean, 2)
visibility_upor_clean = np.insert(visibility_upor_clean, 0, 0)
visibility_udal_clean = np.insert(visibility_udal_clean, 0, 0)
visibility_udal_clean = np.append(visibility_udal_clean, 0)
visibility_upor_clean = np.append(visibility_upor_clean, 0)


plt.figure(figsize=(10, 6))
plt.plot(x_visibility_upor_clean, visibility_upor_clean, color = 'green', label='Упор')
plt.plot(x_visibility_udal_clean, visibility_udal_clean, color = 'blue', label='Удаление')
plt.plot(x_visibility_theor, visibility_theor, color = 'red', label='Теория')
plt.scatter(x_visibility_upor_clean, visibility_upor_clean, color = 'green')
plt.scatter(x_visibility_udal_clean, visibility_udal_clean, color = 'blue')
plt.scatter(x_visibility_theor, visibility_theor, color = 'red')
plt.xlabel('Координата в мм')
plt.ylabel('видность (V)')
plt.title('Видность после удаления шума, нормировка на максимальное значение')
plt.grid(True)
plt.legend()
plt.show()

