import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

#Эта функция удаляет шум из изображения.
#Она принимает ширину изображения (shir), само изображение (im) и шумовое изображение (sh).
#Для каждого столбца (по оси x) вычитает пиксели шумового изображения из исходного изображения и сохраняет результаты в массиве a.
def shumdelete(shir, im, sh):
    a = np.zeros(shir)
    for x in range(shir):
        a[x] = np.sum([(im[y,x])[0] - (sh[y,x])[0] for y in range(vys)])
    return a

#Функции fortheorfunc (для теоретической картинки) и forrealfunc(для реальной картинки):
#Эти функции вычисляют видность на основе минимальных и максимальных значений массива a, который содержит данные после удаления шума.

def fortheorfunc(start, stop, shag, shir):
    V_original = []
    while start < shir:
        I_globmin = np.min(a)
        end = min(stop, shir)
        I_maxval = np.max(a[start:end]) - I_globmin
        I_minval = np.min(a[start:end]) - I_globmin
        # print(f'I_maxval = {I_maxval}, I_minval = {I_minval}, V = {(I_maxval - I_minval) / (I_maxval + I_minval)}')
        V_original.append(1 - (I_maxval - I_minval) / (I_maxval + I_minval))
        start += shag
        stop += shag
    return V_original

def forrealfunc(start, stop, shag, shir):
    V_original = []
    while start < shir:
        I_globmin = np.min(a)
        end = min(stop, shir)
        I_maxval = np.max(a[start:end]) - I_globmin
        I_minval = np.min(a[start:end]) - I_globmin
        # print(f'I_maxval = {I_maxval}, I_minval = {I_minval}, V = {(I_maxval - I_minval) / (I_maxval + I_minval)}')
        V_original.append((I_maxval - I_minval) / (I_maxval + I_minval))
        start += shag
        stop += shag
    return V_original

def graphbuild(x_values, y_values):
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_values, color='red', label = 'видность')
    plt.xlabel('Координата х в пикселях')
    plt.ylabel('Видность')
    plt.title('Зависимость видности от координаты')
    plt.legend()
    plt.grid(True)
    plt.show()

im = cv.imread('image1.png')
sh = cv.imread('shum1.png')
vys, shir, channels = im.shape

a = shumdelete(shir, im, sh)

start = 0
stop = 30
shag = 10

x_values = np.arange(0, len(forrealfunc(start, stop, shag, shir)) * shag, shag)

graphbuild(x_values, forrealfunc(start, stop, shag, shir))

im = cv.imread('image3.png')
vys, shir, channels = im.shape

a = np.zeros(shir)
for x in range(shir):
    a[x] = np.sum([(im[y,x])[0] for y in range(vys)])

start = 0
stop = 10
shag = 2

x2_values = np.arange(0, len(forrealfunc(start, stop, shag, shir)) * shag, shag)

graphbuild(x2_values, fortheorfunc(start, stop, shag, shir))
