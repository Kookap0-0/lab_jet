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
        y = pressure(y)
        x = distance(x)
        return x,y

def find_shift(filename):
    x,y = process(filename)
    return extraFunctions.find_center(x,y)

shift = find_shift(filenames[0])

for i, filename in enumerate(filenames):

    x,y = process(filename)
    x = x - shift

    ax.plot(x, y, 
            color=colors[i % len(colors)], 
            marker=markers[i % len(markers)],
            markersize=2,
            linewidth=1,
            label=filename.replace('.txt', ''))

ax.set_xlabel('Расстояние от центра сопла, мм')
ax.set_ylabel('Давление, Па')
ax.set_title('Зависимость скорости от расстояния до центра сопла')
ax.legend(title='Расстояние от сопла')
ax.grid(True, which='major', color='black', linestyle='-', alpha=0.3)
ax.minorticks_on()
ax.grid(True, which='minor', color='gray', linestyle='--', alpha=0.2)

plt.tight_layout()
plt.show()