import matplotlib.pyplot as plt
from scipy import stats
import numpy as np


filename1 = 'turned_off_calibration.txt'
filename2 = '0mm_calibration.txt'

def filter(filename):
    with open(filename, 'r') as file:
        data = [float(line.strip()) for line in file if line.strip()]
        mean = np.mean(data)
        std = np.std(data)
        filtered_data = []
        for value in data:
            if (np.abs(value-mean)<=3*std):
                filtered_data.append(value)
    with open('filtered_'+filename, 'w') as file:
        for value in filtered_data:
            file.write(f'{value}\n')
    return np.mean(filtered_data)

y1 = filter(filename1)
y2 = filter(filename2)

x1 = 0
x2 = 125 #Па

x = [x1,x2]
y = [y1,y2]

slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
print(slope, intercept)
plt.plot(x,y)
plt.grid()
plt.show()