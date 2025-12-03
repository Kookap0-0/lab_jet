import matplotlib.pyplot as plt
import numpy as np

filename = 'text.txt'
with open(filename, 'r', encoding = 'utf-8') as file:
    data = file.read().strip()
    y = list(map(float, data.split()))
    x = list(range(1, len(y)+1))
plt.ylim(min(y), min(y)*1.05)
plt.plot(x,y)
plt.show()
