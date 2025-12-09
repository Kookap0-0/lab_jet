import matplotlib.pyplot as plt
from scipy import stats
import extraFunctions
import numpy as np

plt.rcParams["font.family"] = "Comfortaa"  


filename1 = 'turned_off_calibration.txt'
filename2 = '0mm_calibration.txt'


extraFunctions.filter(filename1, 3)
extraFunctions.filter(filename2, 3)

def read_filtered_file(filename):
    with open('filtered_' + filename, 'r', encoding='utf-8') as file:
        data = file.read().strip()
        return np.array([float(value) for value in data.split()])

y1_data = read_filtered_file(filename1)
y2_data = read_filtered_file(filename2)

y1 = np.mean(y1_data)
y2 = np.mean(y2_data)

# Pressure values
x1 = 0  # Pa (turned off)
x2 = 125  # Pa (0mm calibration)
#125
x = [x1, x2]
y = [y1, y2]

slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
slope_new = 1/slope
intercept_new = -intercept/slope

def pressure(y):
    y = np.asarray(y, dtype=np.float64)
    return y / slope

if __name__ == "__main__":
    print(f"Slope: {slope_new}")
    print(f"Intercept: {intercept_new}")

    fig, ax = plt.subplots(figsize=(10, 8))

    ax.scatter(x, y, color='orange', s=50, zorder=50, label='Измеренные значения')

    x_fit = np.array([x1, x2])
    y_fit = slope * x_fit + intercept
    ax.plot(x_fit, y_fit, '--', color = '#d62728', linewidth=2, label=f'Fit: P = {slope_new:.4f}N - {-intercept_new:.2f}, Па ')

    equation_text = f'P = {slope_new:.4f}N - {-intercept_new:.2f}, Па'
    ax.text(0.05, 0.95, equation_text, transform=ax.transAxes, 
            fontsize=16, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    ax.set_xlabel('Давление, Па', fontsize = 16)
    ax.set_ylabel('Отсчёты АЦП', fontsize = 16)
    ax.set_title('Калибровка давления', fontsize = 20)
    ax.legend()
    ax.grid(True, which='major', color='black', linestyle='-', alpha=0.3)
    ax.minorticks_on()
    ax.grid(True, which='minor', color='gray', linestyle='--', alpha=0.2)


    plt.tight_layout()
    plt.show()
