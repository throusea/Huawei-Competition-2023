from item import ITEM_INPUT
import numpy as np
def dist(s, d):
    return ((s[0]-d[0]) ** 2 + (s[1]-d[1]) ** 2) ** 0.5

def is_in_set(b: int, b_set: int):
    return (b_set & (1<<b)) != 0

vis = np.zeros(100, 100)

def dfs(i, j, cnt, mp, n):
    if vis[i][j] == 1 or mp[i][j] == 1:
        return

    vis[i][j] = 1
    mp_ret[i][j] = cnt
    if i-1 >= 0:
        dfs(i-1, j, cnt, mp, n)
    if i+1 < n:
        dfs(i+1, j, cnt, mp, n)
    if j-1 >= 0:
        dfs(i, j-1, cnt, mp, n)
    if j+1 < n:
        dfs(i, j+1, cnt, mp, n)

def check_block(n: int, mp: []):
    for i in range(0, n):
        for j in range(0, n):
            vis[i][j] = 0
    cnt = 1
    global mp_ret
    mp_ret = np.zeros(n, n)
    for i in range(0, n):
        for j in range(0, n):
            if vis[i][j] == 0 and mp[i][j] != 1:
                cnt+=1
                dfs(i, j, cnt, mp, n)
    return mp_ret
