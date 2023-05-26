import numpy as np

def euler_to_homomat(point):
    translation = np.array([[1, 0, 0, point[0]],
                            [0, 1, 0, point[1]],
                            [0, 0, 1, point[2]],
                            [0, 0, 0, 1]])
    rotation_x = np.array([[1, 0, 0, 0],
                           [0, np.cos(point[3]), -np.sin(point[3]), 0],
                           [0, np.sin(point[3]), np.cos(point[3]), 0],
                           [0, 0, 0, 1]])
    rotation_y = np.array([[np.cos(point[4]), 0, np.sin(point[4]), 0],
                           [0, 1, 0, 0],
                           [-np.sin(point[4]), 0, np.cos(point[4]), 0],
                           [0, 0, 0, 1]])
    rotation_z = np.array([[np.cos(point[5]), -np.sin(point[5]), 0, 0],
                           [np.sin(point[5]), np.cos(point[5]), 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])
    homogeneous_matrix = translation @ rotation_x @ rotation_y @ rotation_z # python>=3.5 to use @ for matrix multiplication
    return homogeneous_matrix

def euler_from_homomat(homomat):
    translation = homomat[:3, 3]
    rotation_x = np.arctan2(homomat[2, 1], homomat[2, 2])
    rotation_y = np.arctan2(-homomat[2, 0],
                            np.sqrt(homomat[2, 1]**2 + homomat[2, 2]**2))
    rotation_z = np.arctan2(homomat[1, 0], homomat[0, 0])
    x = translation[0]
    y = translation[1]
    z = translation[2]
    R = rotation_x
    P = rotation_y
    Y = rotation_z
    return [x, y, z, R, P, Y]