import numpy as np
from math import pi

def centroid(picture):
    coordinates = np.zeros(2)
    picture = np.array(picture)
    picture = picture / float(np.sum(picture)) 
    (a, b) = picture.shape
    coordinates[0] = np.dot(np.arange(a), np.sum(picture, axis = 1))
    coordinates[1] = np.dot(np.arange(b), np.sum(picture, axis = 0))
    coordinates[0] = int(round(coordinates[0]))
    coordinates[1] = int(round(coordinates[1]))
    return coordinates

def shift_centroid(picture):
    coordinates = centroid(picture)
    (n, m) = picture.shape
    shifted_picture = np.zeros((n, m))
    for i in range(n):
        for j in range(m):
            if (i - n / 2 + coordinates[0] < n) and (j + int(m / 2) - coordinates[1] < m):
                shifted_picture[i, j] = picture[int(i - n / 2 + coordinates[0]), int(j - m / 2 + coordinates[1])]
    return shifted_picture

#Test with a gaussian
    
n = 12
m = 8
gaussian = np.zeros((n, m))
sigma_1 = 1
sigma_2 = 1
mu_1 = 5
mu_2 = 1

for i in range(n):
    for j in range(m):
        gaussian[i, j] = 1. /2 * pi * np.sqrt(sigma_1 * sigma_2) * np.exp(-(mu_1 - i)**2 / (2 * sigma_1)) * np.exp(-(mu_2 - j)**2 / (2 * sigma_2))

print(centroid(shift_centroid(gaussian)))