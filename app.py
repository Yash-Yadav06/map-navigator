"""
Map Navigator - REST API (Flask)

Endpoints
  GET /api/health
  GET /api/cities
  GET /api/roads
  GET /api/route?source=Delhi&destination=Mumbai&algorithm=dijkstra&avoid=Jaipur,Kota
  GET /api/compare?source=Delhi&destination=Mumbai&avoid=...
The frontend (static/index.html) is served from "/".
"""
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from graph_data import CITIES, ROADS, build_graph
from algorithms import ALGORITHMS

app = Flask(__name__, static_folder="static")
CORS(app)

ADJ = build_graph()
WMAP = {(a, b): w for a, nbrs in ADJ.items() for b, w in nbrs}
AVG_SPEED_KMPH = 60


class BadRequest(Exception):
    pass


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify({"error": str(e)}), 400


def parse_query():
    src = request.args.get("source", "").strip()
    dst = request.args.get("destination", "").strip()
    avoid = {c.strip() for c in request.args.get("avoid", "").split(",") if c.strip()}
    for name in (src, dst, *avoid):
        if name not in CITIES:
            raise BadRequest(f"Unknown city: '{name}'")
    if src in avoid or dst in avoid:
        raise BadRequest("Source/destination cannot be in the avoid list")
    return src, dst, avoid


def run(algo, src, dst, avoid):
    if algo not in ALGORITHMS:
        raise BadRequest(f"Unknown algorithm '{algo}'. Use: {', '.join(ALGORITHMS)}")
    res = ALGORITHMS[algo](ADJ, WMAP, src, dst, frozenset(avoid))
    if res["found"]:
        mins = round(res["distance_km"] / AVG_SPEED_KMPH * 60)
        res["eta_hours"], res["eta_minutes"] = divmod(mins, 60)
    return res


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "cities": len(CITIES), "roads": len(ROADS)})


@app.route("/api/cities")
def cities():
    return jsonify([{"name": n, "lat": la, "lon": lo} for n, (la, lo) in sorted(CITIES.items())])


@app.route("/api/roads")
def roads():
    return jsonify([{"from": a, "to": b, "km": WMAP[(a, b)]} for a, b in ROADS])


@app.route("/api/route")
def route():
    src, dst, avoid = parse_query()
    return jsonify(run(request.args.get("algorithm", "dijkstra").lower(), src, dst, avoid))


@app.route("/api/compare")
def compare():
    src, dst, avoid = parse_query()
    return jsonify([run(a, src, dst, avoid) for a in ALGORITHMS])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
