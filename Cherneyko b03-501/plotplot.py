import matplotlib.pyplot as plt
import numpy as np
import extraFunctions


filename = '60mm.txt'
extraFunctions.filter(filename, 3)
with open('filtered_' + filename, 'r', encoding = 'utf-8') as file:
    data = file.read().strip()
    y = list(map(float, data.split()))
    x = list(range(1, len(y)+1))
plt.ylim(min(y), max(y)*1.01)
plt.plot(x,y)
plt.show()
