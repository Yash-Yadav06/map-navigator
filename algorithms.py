"""
Shortest-path algorithms implemented from scratch (DSA core of the project).

dijkstra : min-heap priority queue          O((V + E) log V)
astar    : Dijkstra + haversine heuristic   O(E log V) worst case, usually explores fewer nodes
bfs      : queue, fewest roads/hops         O(V + E)
"""
import heapq
import time
from collections import deque
from math import inf

from graph_data import CITIES, haversine


def _build_result(algo, src, dst, prev, visited, wmap, elapsed):
    if dst != src and dst not in prev:
        return {"algorithm": algo, "found": False, "explored": visited,
                "nodes_explored": len(visited), "time_ms": round(elapsed * 1000, 3)}
    path = [dst]
    while path[-1] != src:
        path.append(prev[path[-1]])
    path.reverse()
    legs = [{"from": a, "to": b, "km": wmap[(a, b)]} for a, b in zip(path, path[1:])]
    return {
        "algorithm": algo, "found": True, "path": path, "legs": legs,
        "distance_km": round(sum(l["km"] for l in legs), 1),
        "hops": len(path) - 1,
        "explored": visited, "nodes_explored": len(visited),
        "time_ms": round(elapsed * 1000, 3),
    }


def dijkstra(adj, wmap, src, dst, blocked):
    t = time.perf_counter()
    dist, prev, done, visited = {src: 0.0}, {}, set(), []
    pq = [(0.0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if u in done:
            continue
        done.add(u)
        visited.append(u)
        if u == dst:
            break
        for v, w in adj[u]:
            if v in blocked or v in done:
                continue
            nd = d + w
            if nd < dist.get(v, inf):
                dist[v], prev[v] = nd, u
                heapq.heappush(pq, (nd, v))
    return _build_result("dijkstra", src, dst, prev, visited, wmap, time.perf_counter() - t)


def astar(adj, wmap, src, dst, blocked):
    t = time.perf_counter()
    h = lambda n: haversine(CITIES[n], CITIES[dst])   # admissible: road >= straight line
    g, prev, done, visited = {src: 0.0}, {}, set(), []
    pq = [(h(src), src)]
    while pq:
        _, u = heapq.heappop(pq)
        if u in done:
            continue
        done.add(u)
        visited.append(u)
        if u == dst:
            break
        for v, w in adj[u]:
            if v in blocked or v in done:
                continue
            ng = g[u] + w
            if ng < g.get(v, inf):
                g[v], prev[v] = ng, u
                heapq.heappush(pq, (ng + h(v), v))
    return _build_result("astar", src, dst, prev, visited, wmap, time.perf_counter() - t)


def bfs(adj, wmap, src, dst, blocked):
    t = time.perf_counter()
    prev, seen, visited = {}, {src}, []
    q = deque([src])
    while q:
        u = q.popleft()
        visited.append(u)
        if u == dst:
            break
        for v, _ in adj[u]:
            if v not in seen and v not in blocked:
                seen.add(v)
                prev[v] = u
                q.append(v)
    return _build_result("bfs", src, dst, prev, visited, wmap, time.perf_counter() - t)


ALGORITHMS = {"dijkstra": dijkstra, "astar": astar, "bfs": bfs}
