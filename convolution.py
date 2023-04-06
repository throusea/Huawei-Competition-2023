import numpy as np
import math
import myutil

p = 0.5

def conv(mat1, mat2):
    r1, c1 = mat1.shape
    r2, c2 = mat2.shape
    mat = np.zeros((r1-r2+1, c1-c2+1))
    dis = np.zeros(mat.shape)
    for i in range(r1-r2+1):
        for j in range(c1-c2+1):
            for k in range(r2):
                for l in range(c2):
                    mat[i][j] += mat1[i+k][j+l] * mat2[k][l]
                    pos[i][j] = get_real_pos((i+p, j+p))
    return mat, pos

def close(r_pos1, r_pos2):
    return myutil.dist(r_pos1, r_pos2)

# def get_grid_pos(real_pos: tuple(float, float)):
#     y = math.floor(pos[0] / v)
#     x = 100 - math.floor(pos[1] / v)
#     return (x, y)

# def get_conv_grid_pos(real_pos: tuple(float, float)):
#     get_grid_pos(real_pos)

def get_real_pos(grid_r_pos: tuple(int, int)):
    return (pos[1], 50-pos[0])