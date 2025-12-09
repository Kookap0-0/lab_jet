import matplotlib.pyplot as plt
import numpy as np
import extraFunctions
from pressure_calibration import pressure
from distance_calibration import distance
plt.rcParams["font.family"] = "Comfortaa"  

fig, ax = plt.subplots(figsize=(12, 8))

colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
markers = ['o', 's', '^', 'd', 'v', '<', '>', 'p']

filenames = ['10mm.txt', '20mm.txt', '30mm.txt', '40mm.txt', 
             '50mm.txt', '60mm.txt', '70mm.txt']


def process(filename):
    extraFunctions.filter(filename, 3)
    
    with open('filtered_' + filename, 'r', encoding='utf-8') as file:
        data = file.read().strip()
        y = list(map(float, data.split()))
        x = list(range(1, len(y) + 1))
        min_y = np.min(y)
        y = pressure(y-min_y)
        x = distance(x)
        return x,y

def find_shift(filename):
    x,y = process(filename)
    return extraFunctions.find_center(x,y)

shift = find_shift(filenames[0])


def first_plot():
    for i, filename in enumerate(filenames):

        x,y = process(filename)
        x = x - shift
        x, y = extraFunctions.remove_outliers(x, y, window=4, threshold=1.5)
        x, y = extraFunctions.remove_lower_outliers(x, y, percentile=3)
        y = y - np.min(y)

        ax.plot(x, y, 
                color=colors[i % len(colors)], 
                marker=markers[i % len(markers)],
                markersize=2,
                linewidth=1,
                label=filename.replace('.txt', ''))
        ax.set_ylabel('Давление, Па', fontsize=18, labelpad=10)

def second_plot():
    for i, filename in enumerate(filenames):

        x,y = process(filename)
        x = x - shift
        x, y = extraFunctions.remove_outliers(x, y, window=4, threshold=1.5)
        x, y = extraFunctions.remove_lower_outliers(x, y, percentile=3) 
        y = y - min(y)

        y = np.sqrt(2*y/1.2)


        area = extraFunctions.integral_to_zero(x, y)
        print(f"Файл {filename}: интеграл до нуля = {2*area}")

        ax.plot(x, y, 
                color=colors[i % len(colors)], 
                marker=markers[i % len(markers)],
                markersize=2,
                linewidth=1,
                label=f"{filename.replace('.txt', '')}, Q = {2*area:.2f} г/с")
        ax.set_ylabel('Скорость, м/c', fontsize=18)

# first_plot()
# second_plot()

ax.set_xlabel('Расстояние от центра сопла, мм', fontsize=18, labelpad=10)
ax.set_title('Зависимость скорости от расстояния до центра сопла', fontsize=22, pad=15)
ax.legend(title='Расстояние от сопла', markerscale=2, fontsize=16, title_fontsize=18)
ax.grid(True, which='major', color='black', linestyle='-', alpha=0.3)
ax.minorticks_on()
ax.grid(True, which='minor', color='gray', linestyle='--', alpha=0.2)

# plt.savefig('velocity.png', dpi=200)
# plt.savefig('pressure.png', dpi=200)
plt.tight_layout()
plt.show()