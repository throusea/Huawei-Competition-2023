import numpy as np
import math
import myutil

p = 0.5

def conv(mat1, mat2):
    r1, c1 = mat1.shape
    r2, c2 = mat2.shape
    k = r2
    mat = np.zeros((r1-r2+1, c1-c2+1))
    dis = np.zeros((r1-r2+1, c1-c2+1, 2))
    for i in range(r1-r2+1):
        for j in range(c1-c2+1):
            for k in range(r2):
                for l in range(c2):
                    mat[i][j] += mat1[i+k][j+l] * mat2[k][l]
                    # print(get_real_pos((i+p, j+p)))
                    dis[i][j] = get_real_pos((i+k*p, j+k*p))
    return mat, dis

def get_cen3(pos, corner):
    return float

def close(r_pos1, r_pos2):
    return myutil.dist(r_pos1, r_pos2) < p

# def get_grid_pos(real_pos: tuple(float, float)):
#     y = math.floor(pos[0] / v)
#     x = 100 - math.floor(pos[1] / v)
#     return (x, y)

# def get_conv_grid_pos(real_pos: tuple(float, float)):
#     get_grid_pos(real_pos)

def get_real_pos(transformed_pos: tuple):
    return (transformed_pos[1]/2, (100 - transformed_pos[0])/2)

def get_transformed_pos(real_pos: tuple):
    return (50-real_pos[1], real_pos[0])

def get_init_pos_2(real_pos: tuple, conv_map2):
    """Description
    get the initial position for the robot in convoluted map.

    Args:
        real_pos (tuple): real position of robot

    Returns:
        list[]: the initial position list for robot
    """
    transformed_pos=get_transformed_pos(real_pos)
    x2_pos=(transformed_pos[0]*2,transformed_pos[1]*2)
    grid_list=[]
    xf=math.floor(x2_pos[0])-1
    xc=math.ceil(x2_pos[0])-1
    yf=math.floor(x2_pos[1])-1
    yc=math.ceil(x2_pos[1])-1
    if xf>=0 and yf>=0 and conv_map2[xf][yf]!=1:
        grid_list.append((xf,yf))
    if xf>=0 and yc<=98 and conv_map2[xf][yc]!=1:
        grid_list.append((xf,yc))
    if xc<=98 and yf>=0 and conv_map2[xc][yf]!=1:
        grid_list.append((xc,yf))
    if xc<=98 and yc<=98 and conv_map2[xc][yc]!=1:
        grid_list.append((xc,yc))
    return grid_list

def get_init_pos_3(real_pos: tuple):
    transformed_pos = get_transformed_pos(real_pos)
    return [(math.floor(transformed_pos[0] * 2) - 1, math.floor(transformed_pos[1] * 2) - 1)]