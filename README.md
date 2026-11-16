# Map Navigator — DSA Minor Project

A web application that finds the shortest route between Indian cities using graph algorithms,
exposed through a REST API and integrated with a Leaflet map frontend.

**Task coverage**
1. *Create a Map Navigator application; deploy API* → Flask REST API (`app.py`) + `Procfile` for deployment.
2. *Integrate backend with frontend using API* → `static/index.html` calls the API with `fetch()` and draws results on the map.

## Data structures & algorithms used
| Concept | Where |
|---|---|
| Graph (adjacency list, weighted, undirected) | `graph_data.build_graph()` — 33 cities (vertices), 57 roads (edges) |
| Min-heap / priority queue (`heapq`) | Dijkstra and A* |
| Queue (`collections.deque`) | BFS |
| Hash map / set | distances, parent pointers, visited sets |
| Dijkstra | shortest distance, O((V+E) log V) |
| A* with haversine heuristic | same optimal answer, explores fewer nodes |
| BFS | route with the fewest roads, O(V+E) |
| Path reconstruction | parent (`prev`) map traced back from destination |

Edge weight = straight-line (haversine) distance × 1.25 road factor (approximation of real road km).
The heuristic never overestimates, so A* is **admissible** and returns the optimal path.

## Run locally
```bash
pip install -r requirements.txt
python app.py
# open http://localhost:5000
```

## API
| Endpoint | Description |
|---|---|
| `GET /api/health` | status |
| `GET /api/cities` | all cities with lat/lon |
| `GET /api/roads` | all roads with km |
| `GET /api/route?source=Delhi&destination=Mumbai&algorithm=dijkstra&avoid=Jaipur,Kota` | route (algorithm: `dijkstra`, `astar`, `bfs`; `avoid` optional) |
| `GET /api/compare?source=Delhi&destination=Mumbai` | runs all three and returns stats |

Example response (`/api/route`): `path`, `legs`, `distance_km`, `hops`, `eta_hours`, `eta_minutes`, `explored`, `nodes_explored`, `time_ms`.

## Deploy the API (Render — free)
1. Push this folder to a GitHub repository.
2. Go to https://render.com → **New → Web Service** → connect the repo.
3. Settings: **Runtime** Python 3, **Build command** `pip install -r requirements.txt`, **Start command** `gunicorn app:app`.
4. Deploy. Your live URL (e.g. `https://map-navigator.onrender.com`) serves both the API and the frontend.
5. Test: `https://<your-url>/api/health`.

(Alternatives: Railway, PythonAnywhere — same files work.)
If you host the frontend elsewhere, set `API_BASE` at the top of the script in `static/index.html` to your API URL (CORS is already enabled).

## Likely viva questions
- **Why Dijkstra over BFS?** BFS ignores weights; it minimises hops, not km. Dijkstra handles non-negative weights.
- **Why a heap?** Gives O(log V) extract-min instead of O(V), so total O((V+E) log V).
- **How is A* better?** The heuristic steers the search toward the goal, so fewer nodes are expanded; still optimal because the heuristic is admissible.
- **Can Dijkstra handle negative edges?** No — use Bellman-Ford.
- **Why adjacency list over matrix?** Road graphs are sparse: O(V+E) space vs O(V²).
- **How does "avoid cities" work?** Blocked nodes are skipped when relaxing edges.
- **Limitations / future work:** real road data (OpenStreetMap), traffic-based weights, turn-by-turn directions, more cities.
