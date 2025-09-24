import time, argparse, heapq, random
from collections import deque

class GridCity:
    def __init__(self,g,start,goal):
        self.grid, self.start, self.goal = g, start, goal
        self.r=len(g); self.c=len(g[0])

    def in_bounds(self,pos):
        r,c=pos
        return 0<=r<self.r and 0<=c<self.c

    def neighbors(self,pos):
        r,c=pos
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r+dr, c+dc
            if self.in_bounds((nr,nc)) and self.grid[nr][nc]!=1:
                yield (nr,nc)

    def cost(self,pos): return self.grid[pos[0]][pos[1]]

def mkpath(prev,s,g):
    if g not in prev: return []
    p=[]; cur=g
    while cur!=None:
        p.append(cur)
        cur=prev[cur]
    return p[::-1]

# bfs
def bfs(city):
    q=deque([city.start]); came={city.start:None}
    while q:
        cur=q.popleft()
        if cur==city.goal: break
        for n in city.neighbors(cur):
            if n not in came:
                came[n]=cur; q.append(n)
    return mkpath(came,city.start,city.goal),len(came)

# ucs
def ucs(city):
    q=[(0,city.start)]
    came={city.start:None}; g={city.start:0}
    while q:
        c,cur=heapq.heappop(q)
        if cur==city.goal: break
        for n in city.neighbors(cur):
            nc=g[cur]+city.cost(n)
            if n not in g or nc<g[n]:
                g[n]=nc; came[n]=cur
                heapq.heappush(q,(nc,n))
    return mkpath(came,city.start,city.goal),g.get(city.goal),len(g)

# astar
def astar(city):
    h=lambda a,b:abs(a[0]-b[0])+abs(a[1]-b[1])
    q=[(0,city.start)]
    came={city.start:None}; g={city.start:0}
    while q:
        _,cur=heapq.heappop(q)
        if cur==city.goal: break
        for n in city.neighbors(cur):
            nc=g[cur]+city.cost(n)
            if n not in g or nc<g[n]:
                g[n]=nc; came[n]=cur
                f=nc+h(n,city.goal)
                heapq.heappush(q,(f,n))
    return mkpath(came,city.start,city.goal),g.get(city.goal),len(g)

# hill climb + restart
def hill(city,steps=150,tries=3):
    h=lambda a,b:abs(a[0]-b[0])+abs(a[1]-b[1])
    best=None; sc=1e9
    for _ in range(tries):
        cur=city.start; path=[cur]
        for _ in range(steps):
            if cur==city.goal: break
            ns=list(city.neighbors(cur))
            if not ns: break
            cur=min(ns,key=lambda n:h(n,city.goal))
            path.append(cur)
        if cur==city.goal and len(path)<sc:
            best,sc=path,len(path)
    return best or [],sc if sc<1e9 else None,len(best or [])

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--algo",choices=["bfs","ucs","astar","hill"],default="bfs")
    args=p.parse_args()

    grid=[[0,0,0,0],
          [0,1,1,0],
          [0,0,2,0],
          [0,0,0,0]]

    city=GridCity(grid,(0,0),(3,3))

    t0=time.time()
    if args.algo=="bfs":
        path,seen=bfs(city); cost=len(path)-1
    elif args.algo=="ucs":
        path,cost,seen=ucs(city)
    elif args.algo=="astar":
        path,cost,seen=astar(city)
    else:
        path,cost,seen=hill(city)
    t1=time.time()

    print("--",args.algo.upper(),"--")
    print("path:",path)
    print("cost:",cost)
    print("visited:",seen)
    print("time:",round(t1-t0,4),"s")
