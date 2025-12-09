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

