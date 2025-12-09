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


def read_filtered_file(filename):
    filter(filename, 3)
    with open('filtered_' + filename, 'r', encoding='utf-8') as f:
        data = f.read().strip().split()
        return np.array(list(map(float, data)))

def find_min(filename):
    data = read_filtered_file(filename)
    return min(data)

def remove_outliers(x, y, window=3, threshold=2.0):
    x = np.asarray(x)
    y = np.asarray(y)
    
    mask = np.ones_like(y, dtype=bool)
    for i in range(len(y)):
        left = max(i - window, 0)
        right = min(i + window + 1, len(y))
        local = y[left:right]
        median = np.median(local)
        mad = np.median(np.abs(local - median))  # robust deviation
        if mad == 0:
            continue
        if abs(y[i] - median) > threshold * mad:
            mask[i] = False
    return x[mask], y[mask]


def remove_lower_outliers(x, y, percentile=5):
    x = np.asarray(x)
    y = np.asarray(y)

    threshold = np.percentile(y, percentile)

    mask = y >= threshold
    return x[mask], y[mask]

def integral_to_zero(x, y):
    x = np.asarray(x)
    y = np.asarray(y)

    idx_zero = np.argmin(np.abs(x))

    if idx_zero > 0:
        x_segment = x[:idx_zero+1]
        y_segment = y[:idx_zero+1]
    else:
        x_segment = x[idx_zero:]
        y_segment = y[idx_zero:]
    
    # Интегрируем методом трапеций
    integral = np.trapezoid(y_segment*np.abs(x_segment), x_segment)
    return integral*2*np.pi*1.2/1000