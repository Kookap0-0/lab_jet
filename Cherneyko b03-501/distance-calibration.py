import matplotlib.pyplot as plt
from scipy import stats


x1 = -360
x2 = 525
y1 = 0
y2 = 5.0

x = [x1,x2]
y = [y1,y2]

slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
print(slope, intercept)
plt.plot(x,y)
plt.grid()
plt.show()