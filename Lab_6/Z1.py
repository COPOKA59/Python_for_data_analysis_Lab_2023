import numpy as np
import pandas as pd

def Z1():
    # 1
    # Создайте Series из последовательности 15 значений, равномерно разбивающих отрезок [0, 20]
    # (воспользуйтесь функцией linspace) (Начальное значение, конечное, сколько нужно элементов получить)
    ser1 = pd.Series(data = np.linspace(0, 20, 15))
    print(f'Series из последовательности 15 значений, равномерно разбивающих отрезок [0, 20] > \n{ser1}')

    # 2
    # Определите отношение элементов полученной серии к их предыдущим элементам (*)
    # Функция Pandas Shift(), сдвигает индекс на желаемое количество периодов.
    # divide — np деление
    ser2 = ser1.divide(ser1.shift(1))
    print(f'\nОтношение элементов полученной серии к их предыдущим элементам > \n{ser2}')

    # 3
    # В результате необходимо получить среднее полученного вектора, оставив в нём только те
    # значения, которые не более чем 1.5 (**)
    # np.mean вычисляет среднее арифметическое
    ser3 = ser2[ser2 <= 1.5].mean()
    print(f'\nСреднее полученного вектора, значения которого не более чем 1.5\n{ser3}')

#Z1()