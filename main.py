import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

# Загрузка изображений. Здесь image1 и image 2 - удаление и упор соответственно
im = cv.imread('image1.png')
shum = cv.imread('shum1.png')

vys, shir, channels = im.shape
a = np.zeros(shir)
s = np.zeros(shir)

# Порог для определения "чёрных" пикселей
chuvstv = 7
ch = np.array([0, 0, 0])

# Функция для определения чёрного пикселя с учётом порога
def is_black(pixel, chuvstv):
    return np.all(pixel <= chuvstv)

# Суммируем нечёрные пиксели в исходнике
for x in range(shir):
    a[x] = np.sum([not is_black(im[y, x], chuvstv) for y in range(vys)])

# Суммируем нечёрные пиксели в шуме
for x in range(shir):
    s[x] = np.sum([not is_black(shum[y, x], chuvstv) for y in range(vys)])

# Расчёт видимости для исходного изображения
start = 0
stop = 5
shag = 5
V_original = []

while start < shir:
    end = min(stop, shir)
    I_maxval = np.max(a[start:end])
    I_minval = np.min(a[start:end])
    if I_minval + I_maxval == 0 or I_minval < 5:
        V_original.append(0)
    else:
        V_original.append((I_maxval - I_minval) / (I_maxval + I_minval))
    start += shag
    stop += shag

# Создаём скорректированное изображение
corrected_image = np.copy(im)
for x in range(shir):
    if s[x] > 0:
        for y in range(vys):
            # Берём нечёрный пиксель в шуме с координатами [y,x], заменяем оригинальный пиксель с координатами [y,x] на чёрный
            if not is_black(shum[y, x], chuvstv):
                corrected_image[y, x] = ch

# Сохранение нового изображения после удаления шума
cv.imwrite('image_corrected.png', corrected_image)

#Делаем замену
im = corrected_image

b = np.copy(a)
# Вычитаем шумовые пиксели из оригинального массива нечёрных пикселей а
a = np.clip(a - s, 0, None)

# Считаем видность после удаления шума
start = 0
stop = 5
V_corrected = []

while start < shir:
    end = min(stop, shir)
    I_maxval = np.max(a[start:end])
    I_minval = np.min(a[start:end])
    if I_minval + I_maxval == 0 or I_minval < 5:
        V_corrected.append(0)
    else:
        ## отладка:
        # print(f'I_maxval = {I_maxval}, I_minval = {I_minval}, V = {(I_maxval - I_minval) / (I_maxval + I_minval)}')
        V_corrected.append((I_maxval - I_minval) / (I_maxval + I_minval))
    start += shag
    stop += shag

# Построение графиков
x_values = np.arange(0, len(V_original) * shag, shag)

plt.figure(figsize=(10, 6))
plt.plot(x_values, b, label='С исходным изображением', color='blue')
plt.plot(x_values, a, label='После удаления шума', color='red')
plt.xlabel('Координата х в пикселях')
plt.ylabel('Интенсивность')
plt.title('Сравнение интенсивности до и после удаления шума (упор)')
plt.legend()
plt.grid(True)
plt.show()