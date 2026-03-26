from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GEOCODIO_KEY = os.getenv('GEOCODIO_KEY') or "a6764eeee99779eda67d4c6a996549e5c656d5c"

@app.route('/scan', methods=['GET', 'POST'])
def scan():
    address = request.form.get('address') or request.json.get('address')
    if not address:
        return jsonify({"error": "No address"}), 400

    # Geocode
    geo_url = f"https://api.geocod.io/v1.12/geocode?q={address}&api_key={GEOCODIO_KEY}"
    geo_resp = requests.get(geo_url)
    if geo_resp.status_code != 200 or not geo_resp.json().get('results'):
        return jsonify({"error": "Geocode failed"}), 500

    loc = geo_resp.json()['results'][0]['location']
    lat, lng = loc['lat'], loc['lng']

    # FEMA flood
    fema_url = f"https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28/query?geometry={lng},{lat}&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=FLOOD_ZONE,SFHA_TF&f=json"
    fema_resp = requests.get(fema_url)
    if fema_resp.status_code != 200:
        return jsonify({"error": "FEMA failed"}), 500

    features = fema_resp.json().get('features', [])
    if features:
        zone = features[0]['attributes'].get('FLOOD_ZONE', 'Unknown')
        sfha = features[0]['attributes'].get('SFHA_TF') == 'T'
        risk = "high" if zone in ["A", "AE", "V"] or sfha else "low"
        reason = f"Flood zone: {zone} (SFHA: {'Yes' if sfha else 'No'})"
    else:
        risk = "low"
        reason = "No flood data"

    return jsonify({
        "risk_level": risk,
        "reason": reason,
        "lat": lat,
        "lng": lng,
        "address": address
    })

if __name__ == '__main__':
    app.run(debug=True)

application = app  # Vercel hook
```

---

## What was broken and why

| Bug | Original | Fixed |
|---|---|---|
| Empty `methods` | `methods= )` | `methods=['GET', 'POST']` |
| Wrong geocode result access | `geo_resp.json()[0]` | `geo_resp.json()['results'][0]['location']` |
| Missing dict keys for lat/lng | `loc , loc` | `loc['lat'], loc['lng']` |
| Broken feature attribute access | `features[0 0]['attributes' "A"...]` | Proper indexing + `.get()` |
| `risk` variable never set in `if` block | logic was garbled | Properly assigns `risk` and `sfha` |

---

## Also make sure you have a `requirements.txt`:
```
flask
requests

@app.route('/')
def home():
return jsonify({"status": "NexGen Pro Dynamics API is running!"})
fema_url = f"https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28/query?geometry={lng},{lat}&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=FLOOD_ZONE,SFHA_TF&f=json"
risk = "high" if zone in or sfha else "low"

