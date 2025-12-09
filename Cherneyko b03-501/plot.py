import matplotlib.pyplot as plt
import numpy as np
import extraFunctions
from pressure_calibration import pressure
from distance_calibration import distance
plt.rcParams["font.family"] = "Comfortaa"  

fig, ax = plt.subplots(figsize=(12, 8))

colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
markers = ['o', 's', '^', 'd', 'v', '<', '>', 'p']

filenames = ['0mm.txt','10mm.txt', '20mm.txt', '30mm.txt', '40mm.txt', 
             '50mm.txt', '60mm.txt', '70mm.txt']

Q = []


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
    ax.set_xlabel('Расстояние от центра сопла, мм', fontsize=18, labelpad=10)
    ax.set_title('Зависимость давления от расстояния до центра сопла', fontsize=22, pad=15)
    ax.legend(title='Расстояние от сопла', markerscale=2, fontsize=16, title_fontsize=18)

def second_plot():
    for i, filename in enumerate(filenames):

        x,y = process(filename)
        x = x - shift
        x, y = extraFunctions.remove_outliers(x, y, window=4, threshold=1)
        x, y = extraFunctions.remove_lower_outliers(x, y, percentile=3) 
        y = y - min(y)

        y = np.sqrt(2*y/1.2)


        area = extraFunctions.integral_to_zero(x, y)
        Q.append(area)
        print(f"Файл {filename}: интеграл до нуля = {2*area}")

        ax.plot(x, y, 
                color=colors[i % len(colors)], 
                marker=markers[i % len(markers)],
                markersize=2,
                linewidth=1,
                label=f"{filename.replace('.txt', '')}, Q = {2*area:.2f} г/с")
        ax.set_ylabel('Скорость, м/c', fontsize=18)
        with open("Q_values.txt", "w", encoding="utf-8") as f:
            for i, area in enumerate(Q):
                f.write(f"{i*10}; {2*area:.4f}\n")
    ax.set_xlabel('Расстояние от центра сопла, мм', fontsize=18, labelpad=10)
    ax.set_title('Зависимость скорости от расстояния до центра сопла', fontsize=22, pad=15)
    ax.legend(title='Расстояние от сопла', markerscale=2, fontsize=16, title_fontsize=18)

def third_plot(filename="Q_values.txt"):
    x_vals = []
    y_vals = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():  # пропускаем пустые строки
                x, y = line.strip().split(";")
                x_vals.append(float(x))
                y_vals.append(float(y))

    ax.plot(x_vals, y_vals, 'o--', color='#d62728',markerfacecolor='orange',markeredgecolor='orange', linewidth=1, markersize=9)
    ax.set_xlabel('Расстояние от сопла, мм', fontsize=16)
    ax.set_ylabel('Массовый расход Q, г/с', fontsize=16)
    ax.set_title('Зависимость массового расхода от расстояния до сопла', fontsize=18, pad=15)

first_plot()
# second_plot()
# third_plot()


# ax.legend(title='Расстояние от сопла', markerscale=2, fontsize=16, title_fontsize=18)
ax.grid(True, which='major', color='black', linestyle='-', alpha=0.3)
ax.minorticks_on()
ax.grid(True, which='minor', color='gray', linestyle='--', alpha=0.2)


plt.savefig('pressure.png', dpi=200)
# plt.savefig('velocity.png', dpi=200)
# plt.savefig('q.png', dpi=200)
plt.tight_layout()
plt.show()