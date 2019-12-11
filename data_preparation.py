import numpy as np
from numpy import reshape

### First, we have to take into account a black and white picture aka a 2D-array

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

### Now, the methods are made for every type of array

def lineic_encoding(picture, vertical):
    picture = np.array(picture)
    size = picture.size
    if vertical == False:
        encoded_picture = picture.reshape((1, size))
    else:
        encoded_picture = np.transpose(picture).reshape((1, size))
    return encoded_picture[0]


def is_stochastic_vector(distribution): #is the given array a stochastic vector ? Must be normalized (norm 1)
    distribution = np.array(distribution)
    size = distribution.size
    distribution = lineic_encoding(distribution, vertical=False)
    is_stochastic_vector = False
    is_normalized = False
    is_positive = True
    if np.isclose(sum(distribution), 1, atol=1e-04):
        is_normalized = True
    for i in range(size):
        if distribution[i] < 0:
            is_positive = False
    if is_normalized == True and is_positive == True:
        is_stochastic_vector = True
    return is_stochastic_vector


def stochastic_vector_from_angles(angles): #create a stochastic vector from angles by noting that a stochastic vector is just the square of a hyperspheric vector
    stochastic_distribution = []
    angles = list(angles)
    angles.append(0)
    for i in range(len(angles)):
        inter = np.cos(angles[i])
        for j in range(i):
            inter = inter * np.sin(angles[j])
        stochastic_distribution.append(inter ** 2)
    return stochastic_distribution