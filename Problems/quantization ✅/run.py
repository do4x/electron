import numpy as np

# Load the file
data = np.load('quantization_station.npz')

# View available arrays
print(data.files)

# Access specific arrays
for key in data.files:
    array = data[key]
    print(f"{key}: shape={array.shape}, dtype={array.dtype}")