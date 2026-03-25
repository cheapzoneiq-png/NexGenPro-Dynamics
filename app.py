from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Securely load key from env (add it in Vercel settings later)
GEOCODIO_KEY = os.getenv('GEOCODIO_KEY')

@app.route('/scan', methods= )
def scan():
address = request.form.get('address') or request.json.get('address')
if not address:
return jsonify({"error": "No address provided"}), 400

# Step 1: Geocode with Geocodio
geo_url = f"https://api.geocod.io/v1.12/geocode?q={address}&api_key={GEOCODIO_KEY}"
geo_resp = requests.get(geo_url)
if geo_resp.status_code != 200:
return jsonify({"error": "Geocode failed", "details": geo_resp.text}), 500

geo_data = geo_resp.json()
if not geo_data.get('results'):
return jsonify({"error": "No location found for address"}), 404

# Get first result's lat/lng
location = geo_data [0] lat = location lng = location # Step 2: Query FEMA NFHL for flood zone
fema_url = (
f"https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28/query?"
f"geometry={lng},{lat}&geometryType=esriGeometryPoint&inSR=4326&"
f"spatialRel=esriSpatialRelIntersects&outFields=FLOOD_ZONE,SFHA_TF&f=json"
)
fema_resp = requests.get(fema_url)
if fema_resp.status_code != 200:
return jsonify({"error": "FEMA query failed", "details": fema_resp.text}), 500

fema_data = fema_resp.json()
features = fema_data.get('features', [ 0] .get('FLOOD_ZONE', 'Unknown')
sfha = features[0] .get('SFHA_TF', 'N') == 'T' # T = True
risk = "high" if zone in or sfha else "low"
reason = f"Flood zone: {zone} (Special Flood Hazard Area: {'Yes' if sfha else 'No'})"
else:
risk = "low"
reason = "No flood data found"

return jsonify({
"risk_level": risk,
"reason": reason,
"lat": lat,
"lng": lng,
"address": address
})

if __name__ == '__main__':
app.run(debug=True)

# Vercel hook - required for deployment
application = app
