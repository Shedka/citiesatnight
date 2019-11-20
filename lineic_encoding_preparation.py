import numpy as np
from numpy import reshape

def lineic_encoding(picture, vertical):
    picture = np.array(picture)
    (a, b) = picture.shape
    if vertical == False:
        encoded_picture = picture.reshape((1, a*b))
    else:
        encoded_picture = np.transpose(picture).reshape((1, a*b))
    return encoded_picture

#Test of the lineic encoding

A = [[1, 2, 3],[4, 5, 6], [7, 8, 9]]

print(lineic_encoding(A, vertical=False))
