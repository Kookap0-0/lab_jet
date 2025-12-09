import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

plt.rcParams["font.family"] = "Comfortaa"  

x1 = -360
x2 = 525
y1 = 0
y2 = 5.0

x = [x1, x2]
y = [y1, y2]

slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

def distance(y):
    y = np.asarray(y, dtype=np.float64)
    return slope*y*4*10

if __name__ == "__main__":
        print(f"Угловой коэффициент (slope): {0.01*slope:.6f}")
        print(f"Свободный член (intercept): {0.01*intercept:.6f}")

        x_range = np.linspace(min(x1, x2) - 50, max(x1, x2) + 50, 100)
        y_range = slope * x_range + intercept

        fig, ax = plt.subplots(figsize=(10, 8))

        ax.scatter(x, y, color='orange', s=100, zorder=5, label='Исходные точки')

        ax.plot(x_range, y_range, '--', color = '#d62728', linewidth=2, label=f'y = {slope:.4f}x + {intercept:.4f}, см')



        equation_text = f'y = {slope:.4f}x + {intercept:.4f}, см'
        ax.text(0.05, 0.95, equation_text, transform=ax.transAxes, 
                fontsize=16, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

        ax.set_xlabel('Количество шагов', fontsize=16, labelpad=10)
        ax.set_ylabel('Перемещение трубки Пито, см', fontsize=16, labelpad=10)
        ax.set_title('Калибровочный график зависимости \n перемещения трубки Пито от шага двигателя', fontsize=20)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        ax.grid(True, which='major', color='black', linestyle='-', alpha=0.3)
        ax.minorticks_on()
        ax.grid(True, which='minor', color='gray', linestyle='--', alpha=0.2)


        plt.tight_layout()
        plt.show()
