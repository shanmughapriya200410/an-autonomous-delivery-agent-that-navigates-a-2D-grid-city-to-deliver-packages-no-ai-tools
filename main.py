
# Python Code (`city_agent.py`)  

```python
import time, argparse, heapq, random
from collections import deque

class GridCity:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.rows = len(grid)
        self.cols = len(grid[0])

    def in_bounds(self, pos):
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def neighbors(self, pos):
        r,c = pos
        moves = [(1,0),(-1,0),(0,1),(0,-1)]
        for dr, dc in moves:
            nr, nc = r+dr, c+dc
            if self.in_bounds((nr,nc)) and self.grid[nr][nc] != 1:
                yield (nr,nc)

    def cost(self, pos):
        return self.grid[pos[0]][pos[1]]

def build_path(came,start,goal):
    if goal not in came: return []
    path, cur = [], goal
    while cur is not None:
        path.append(cur)
        cur = came[cur]
    return path[::-1]

# --- BFS ---
def bfs(city):
    q = deque([city.start])
    came = {city.start: None}
    while q:
        cur = q.popleft()
        if cur == city.goal: break
        for n in city.neighbors(cur):
            if n not in came:
                came[n] = cur
                q.append(n)
    return build_path(came, city.start, city.goal), len(came)

# --- UCS ---
def ucs(city):
    q = [(0, city.start)]
    came, cost_map = {city.start: None}, {city.start: 0}
    while q:
        cost, cur = heapq.heappop(q)
        if cur == city.goal: break
        for n in city.neighbors(cur):
            newc = cost_map[cur] + city.cost(n)
            if n not in cost_map or newc < cost_map[n]:
                cost_map[n] = newc
                heapq.heappush(q,(newc,n))
                came[n] = cur
    return build_path(came, city.start, city.goal), cost_map.get(city.goal), len(came)

# --- A* ---
def astar(city):
    h = lambda a,b: abs(a[0]-b[0])+abs(a[1]-b[1])
    q = [(0, city.start)]
    came, cost_map = {city.start: None}, {city.start: 0}
    while q:
        _, cur = heapq.heappop(q)
        if cur == city.goal: break
        for n in city.neighbors(cur):
            newc = cost_map[cur] + city.cost(n)
            if n not in cost_map or newc < cost_map[n]:
                cost_map[n] = newc
                f = newc + h(n, city.goal)
                heapq.heappush(q,(f,n))
                came[n] = cur
    return build_path(came, city.start, city.goal), cost_map.get(city.goal), len(came)

# --- Hill Climb with random restarts ---
def hill_climb(city, max_steps=200, restarts=5):
    def h(a,b): return abs(a[0]-b[0])+abs(a[1]-b[1])
    best_path = None
    best_score = float("inf")
    for _ in range(restarts):
        cur = city.start
        path = [cur]
        steps = 0
        while cur != city.goal and steps < max_steps:
            neigh = list(city.neighbors(cur))
            if not neigh: break
            cur = min(neigh, key=lambda n: h(n,city.goal))
            path.append(cur)
            steps += 1
        if cur == city.goal and len(path) < best_score:
            best_path = path
            best_score = len(path)
    return best_path if best_path else [], best_score if best_score!=float("inf") else None, len(best_path or [])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--algo", choices=["bfs","ucs","astar","hill"], default="bfs")
    args = parser.parse_args()

    # sample grid: 0 free, 1 block, >1 = cost
    grid = [
        [0,0,0,0],
        [0,1,1,0],
        [0,0,2,0],
        [0,0,0,0]
    ]
    city = GridCity(grid,(0,0),(3,3))

    t0 = time.time()
    if args.algo=="bfs":
        path, explored = bfs(city)
        cost = len(path)-1
    elif args.algo=="ucs":
        path, cost, explored = ucs(city)
    elif args.algo=="astar":
        path, cost, explored = astar(city)
    else:
        path, cost, explored = hill_climb(city)
    t1 = time.time()

    print("Algorithm:", args.algo.upper())
    print("Path:", path)
    print("Cost:", cost)
    print("Visited:", explored)
    print("Time:", round(t1-t0,4),"s")
```
