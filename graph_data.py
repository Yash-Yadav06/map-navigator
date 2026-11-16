"""
Road network data for the Map Navigator.

CITIES : name -> (latitude, longitude)
ROADS  : list of (city_a, city_b) direct highway links (bidirectional)

Road distance is estimated as straight-line (haversine) distance * ROAD_FACTOR,
because real roads are never perfectly straight. This also keeps the A*
heuristic (pure haversine) admissible.
"""
from math import radians, sin, cos, asin, sqrt

ROAD_FACTOR = 1.25

CITIES = {
    "Delhi": (28.6139, 77.2090), "Gurugram": (28.4595, 77.0266),
    "Noida": (28.5355, 77.3910), "Ghaziabad": (28.6692, 77.4538),
    "Faridabad": (28.4089, 77.3178), "Meerut": (28.9845, 77.7064),
    "Mathura": (27.4924, 77.6737), "Agra": (27.1767, 78.0081),
    "Gwalior": (26.2183, 78.1828), "Jhansi": (25.4484, 78.5685),
    "Jaipur": (26.9124, 75.7873), "Ajmer": (26.4499, 74.6399),
    "Udaipur": (24.5854, 73.7125), "Jodhpur": (26.2389, 73.0243),
    "Kota": (25.2138, 75.8648), "Ahmedabad": (23.0225, 72.5714),
    "Surat": (21.1702, 72.8311), "Mumbai": (19.0760, 72.8777),
    "Pune": (18.5204, 73.8567), "Indore": (22.7196, 75.8577),
    "Bhopal": (23.2599, 77.4126), "Nagpur": (21.1458, 79.0882),
    "Chandigarh": (30.7333, 76.7794), "Ambala": (30.3782, 76.7767),
    "Ludhiana": (30.9010, 75.8573), "Amritsar": (31.6340, 74.8723),
    "Dehradun": (30.3165, 78.0322), "Haridwar": (29.9457, 78.1642),
    "Lucknow": (26.8467, 80.9462), "Kanpur": (26.4499, 80.3319),
    "Prayagraj": (25.4358, 81.8463), "Varanasi": (25.3176, 82.9739),
    "Patna": (25.5941, 85.1376),"Hyderabad": (17.3850, 78.4867),
    "Bengaluru": (12.9716, 77.5946),"Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639),"Raipur": (21.2514, 81.6296),
    "Ranchi": (23.3441, 85.3096),"Guwahati": (26.1445, 91.7362),
}

ROADS = [
    # Delhi NCR
    ("Delhi", "Gurugram"), ("Delhi", "Noida"), ("Delhi", "Ghaziabad"),
    ("Delhi", "Faridabad"), ("Noida", "Ghaziabad"), ("Gurugram", "Faridabad"),
    ("Noida", "Faridabad"), ("Ghaziabad", "Meerut"), ("Delhi", "Meerut"),
    # Delhi - Agra - Gwalior corridor
    ("Faridabad", "Mathura"), ("Delhi", "Mathura"), ("Mathura", "Agra"),
    ("Noida", "Agra"), ("Agra", "Gwalior"), ("Gwalior", "Jhansi"),
    ("Jhansi", "Bhopal"), ("Gwalior", "Bhopal"),
    # Rajasthan
    ("Delhi", "Jaipur"), ("Gurugram", "Jaipur"), ("Agra", "Jaipur"),
    ("Jaipur", "Ajmer"), ("Ajmer", "Jodhpur"), ("Ajmer", "Udaipur"),
    ("Jodhpur", "Udaipur"), ("Jaipur", "Kota"), ("Kota", "Udaipur"),
    ("Kota", "Indore"), ("Kota", "Bhopal"),
    # Gujarat / Maharashtra / MP
    ("Udaipur", "Ahmedabad"), ("Jodhpur", "Ahmedabad"), ("Ahmedabad", "Surat"),
    ("Surat", "Mumbai"), ("Mumbai", "Pune"), ("Ahmedabad", "Indore"),
    ("Indore", "Bhopal"), ("Bhopal", "Nagpur"), ("Indore", "Surat"),
    ("Pune", "Indore"),
    # Punjab / Haryana / Uttarakhand
    ("Delhi", "Ambala"), ("Delhi", "Chandigarh"), ("Ambala", "Chandigarh"),
    ("Ambala", "Ludhiana"), ("Chandigarh", "Ludhiana"), ("Ludhiana", "Amritsar"),
    ("Meerut", "Haridwar"), ("Haridwar", "Dehradun"), ("Chandigarh", "Dehradun"),
    # Uttar Pradesh / Bihar
    ("Delhi", "Lucknow"), ("Agra", "Lucknow"), ("Agra", "Kanpur"),
    ("Lucknow", "Kanpur"), ("Kanpur", "Prayagraj"), ("Lucknow", "Prayagraj"),
    ("Prayagraj", "Varanasi"), ("Lucknow", "Varanasi"), ("Varanasi", "Patna"),
    ("Kanpur", "Jhansi"),
]


def haversine(a, b):
    """Great-circle distance in km between two (lat, lon) points."""
    lat1, lon1, lat2, lon2 = map(radians, (*a, *b))
    h = sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2
    return 2 * 6371.0 * asin(sqrt(h))


def build_graph():
    """Return adjacency list: {city: [(neighbour, road_km), ...]}"""
    adj = {c: [] for c in CITIES}
    for a, b in ROADS:
        w = round(haversine(CITIES[a], CITIES[b]) * ROAD_FACTOR, 1)
        adj[a].append((b, w))
        adj[b].append((a, w))
    return adj
