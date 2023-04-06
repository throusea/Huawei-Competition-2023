from item import ITEM_INPUT
import numpy as np
def dist(s, d):
    return ((s[0]-d[0]) ** 2 + (s[1]-d[1]) ** 2) ** 0.5

def is_in_set(b: int, b_set: int):
    return (b_set & (1<<b)) != 0

def bfs(i, j, cnt, n):
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
        if (x + 1 < n):
            s += 1
            q.append((x+1, y))
        if (y - 1 >= 0):
            s += 1
            q.append((x, y-1))
        if (y + 1 < n):
            s += 1
            q.append((x, y+1))

def check_block(n: int, mp):
    global vis
    vis = np.zeros((n, n), dtype=int)
    for i in range(0, n):
        for j in range(0, n):
            vis[i][j] = 0
    cnt = 1
    global mmp
    mmp = mp
    global mp_ret
    mp_ret = np.zeros((n, n), dtype=int)
    for i in range(0, n):
        for j in range(0, n):
            if vis[i][j] == 0 and mp[i][j] != 1:
                cnt+=1
                bfs(i, j, cnt, n)
    return mp_ret
