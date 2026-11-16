import json
import urllib.parse
import urllib.request
from math import radians, sin, cos, asin, sqrt

# 1. Fetch all cities in India from OpenStreetMap Overpass API
# Tip: Change ["place"="city"] to ["place"~"city|town"] to get 4,000+ cities & towns!
query = """
[out:json][timeout:60];
node["place"="city"](6.5,68.0,35.5,97.5);
out body;
"""

print("Downloading cities from OpenStreetMap Overpass API...")
url = "https://overpass-api.de/api/interpreter"
data = urllib.parse.urlencode({"data": query}).encode("utf-8")
req = urllib.request.Request(url, data=data, headers={"User-Agent": "MapNavigatorDSA/1.0"})

with urllib.request.urlopen(req, timeout=60) as resp:
    osm_data = json.loads(resp.read().decode("utf-8"))

cities = {}
for el in osm_data["elements"]:
    tags = el.get("tags", {})
    name = tags.get("name:en") or tags.get("name")
    if name:
        # Clean whitespace and avoid duplicate city names
        name = name.strip()
        if name not in cities:
            cities[name] = [round(el["lat"], 4), round(el["lon"], 4)]

print(f"Fetched {len(cities)} unique cities.")

# 2. Auto-connect each city to its 5 nearest neighbors using Haversine distance
def haversine(a, b):
    lat1, lon1, lat2, lon2 = map(radians, (*a, *b))
    h = sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2
    return 2 * 6371.0 * asin(sqrt(h))

roads = set()
city_items = list(cities.items())

for i, (name_a, coord_a) in enumerate(city_items):
    # Find the 5 closest neighboring cities
    distances = []
    for j, (name_b, coord_b) in enumerate(city_items):
        if i != j:
            distances.append((haversine(coord_a, coord_b), name_b))
    distances.sort()
    for _, neighbor in distances[:5]:
        roads.add(tuple(sorted((name_a, neighbor))))

# 3. Save to map_data.json
with open("map_data.json", "w", encoding="utf-8") as f:
    json.dump({"cities": cities, "roads": [list(r) for r in sorted(roads)]}, f, indent=2)

print(f"Saved {len(cities)} cities and {len(roads)} roads to map_data.json!")