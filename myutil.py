from item import ITEM_INPUT
import numpy as np
def dist(s, d):
    return ((s[0]-d[0]) ** 2 + (s[1]-d[1]) ** 2) ** 0.5

def is_in_set(b: int, b_set: int):
    return (b_set & (1<<b)) != 0

def bfs(i, j, cnt, w, h, vis, mmp, mp_ret):
    q = []
    s = 0
    r = 0
    q.append((i, j))
    while(r <= s):
        x = (int)(q[r][0])
        y = (int)(q[r][1])
        r += 1
        if vis[x][y] == 1 or mmp[x][y] == 1:
            continue
        vis[x][y] = 1
        mp_ret[x][y] = cnt
        if(x-1 >= 0):
            s+=1
            q.append((x-1, y))
        if (x + 1 < w):
            s += 1
            q.append((x+1, y))
        if (y - 1 >= 0):
            s += 1
            q.append((x, y-1))
        if (y + 1 < h):
            s += 1
            q.append((x, y+1))

def check_block(mp):
    w, h = mp.shape
    mmp = np.zeros(mp.shape)
    vis = np.zeros((w, h), dtype=int)
    for i in range(0, w):
        for j in range(0, h):
            vis[i][j] = 0
            mmp[i][j] = 1 if mp[i][j] >= 1 else 0
    cnt = 1
    mp_ret = np.zeros((w, h), dtype=int)
    for i in range(0, w):
        for j in range(0, h):
            if vis[i][j] == 0 and mmp[i][j] != 1:
                cnt+=1
                bfs(i, j, cnt, w, h, vis, mmp, mp_ret)
    return mp_ret
