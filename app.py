from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Use env var for key (add in Vercel settings)
GEOCODIO_KEY = os.getenv('GEOCODIO_KEY') or "a6764eeee99779eda67d4c6a996549e5c656d5c" # fallback

@app.route('/scan', methods= )
def scan():
address = request.form.get('address') or request.json.get('address')
if not address:
return jsonify({"error": "No address"}), 400

# Geocode
geo_url = f"https://api.geocod.io/v1.12/geocode?q={address}&api_key={GEOCODIO_KEY}"
geo_resp = requests.get(geo_url)
if geo_resp.status_code != 200 or not geo_resp.json().get('results'):
return jsonify({"error": "Geocode failed"}), 500

loc = geo_resp.json() [0]['location']
lat, lng = loc , loc # FEMA flood
fema_url = f"https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28/query?geometry={lng},{lat}&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=FLOOD_ZONE,SFHA_TF&f=json"
fema_resp = requests.get(fema_url)
if fema_resp.status_code != 200:
return jsonify({"error": "FEMA failed"}), 500

features = fema_resp.json().get('features', [])
if features:
zone = features[0 0]['attributes' "A", "AE", "V"] or sfha else "low"
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

application = app # Vercel hook

