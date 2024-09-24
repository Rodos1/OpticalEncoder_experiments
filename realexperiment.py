#Почти тот же код, только без проверки и удаления шумовых пикселей

import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

def is_black(pixel, chuvstv):
    return np.all(pixel <= chuvstv)

im = cv.imread('image3.png')
vys, shir, channels = im.shape
a = np.zeros(shir)

chuvstv = 80
ch = np.array([0, 0, 0])

# Суммируем нечёрные пиксели в исходнике
for x in range(shir):
    a[x] = np.sum([not is_black(im[y, x], chuvstv) for y in range(vys)])

# Расчёт видимости для исходного изображения
start = 0
stop = 5
shag = 5
V_original = []

while start < shir:
    end = min(stop, shir)
    I_maxval = np.max(a[start:end])
    I_minval = np.min(a[start:end])
    if I_minval + I_maxval == 0:
        V_original.append(0)
    elif abs(I_minval-I_maxval) < 1:
        V_original.append(1)
    else:
        print(f'I_maxval = {I_maxval}, I_minval = {I_minval}, V = {(I_maxval - I_minval) / (I_maxval + I_minval)}')
        V_original.append((I_maxval - I_minval) / (I_maxval + I_minval))
    start += shag
    stop += shag

x_values = np.arange(0, len(V_original) * shag, shag)

plt.figure(figsize=(10, 6))
plt.plot(x_values, V_original, color='red')
plt.xlabel('Координата х в пикселях')
plt.ylabel('Видность')
plt.title('Зависимость видности от координаты')
plt.legend()
plt.grid(True)
plt.show()