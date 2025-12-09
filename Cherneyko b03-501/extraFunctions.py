import numpy as np

def filter(filename,n):
    with open(filename, 'r') as file:
        data = [float(line.strip()) for line in file if line.strip()]
        mean = np.mean(data)
        std = np.std(data)
        filtered_data = []
        for value in data:
            if (np.abs(value-mean)<=n*std):
                filtered_data.append(value)
    with open('filtered_'+filename, 'w') as file:
        for value in filtered_data:
            file.write(f'{value}\n')

# def find_center(x, y):
#     x = np.asarray(x)
#     y = np.asarray(y)
    
#     y = y - np.min(y)
#     if np.sum(y) == 0:
#         return None
    
#     center = np.sum(x * y) / np.sum(y)
#     return center

def find_center(x, y, top_fraction=0.25):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    ymin = np.min(y)
    ymax = np.max(y)
    if ymax == ymin:
        return None

    cutoff = ymax - (ymax - ymin) * top_fraction

    mask = y >= cutoff
    if np.sum(mask) == 0:
        return None

    x_top = x[mask]
    y_top = y[mask]

    center = np.sum(x_top * y_top) / np.sum(y_top)
    return center
