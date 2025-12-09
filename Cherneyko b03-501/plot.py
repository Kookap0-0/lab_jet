import matplotlib.pyplot as plt
import numpy as np
import extraFunctions
from pressure_calibration import pressure
from distance_calibration import distance

fig, ax = plt.subplots(figsize=(12, 8))

colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
markers = ['o', 's', '^', 'd', 'v', '<', '>', 'p']

filenames = ['10mm.txt', '20mm.txt', '30mm.txt', '40mm.txt', 
             '50mm.txt', '60mm.txt', '70mm.txt']

for i, filename in enumerate(filenames):
    extraFunctions.filter(filename, 3)
    
    with open('filtered_' + filename, 'r', encoding='utf-8') as file:
        data = file.read().strip()
        y = list(map(float, data.split()))
        x = list(range(1, len(y) + 1))
        y = pressure(y)
        x = distance(x)

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
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()