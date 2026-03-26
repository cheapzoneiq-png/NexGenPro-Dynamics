
@app.route('/scan', methods= )
def scan():
try:
address = request.form.get('address') or request.json.get('address')
if not address:
return jsonify({"error": "No address"}), 400

geo_url = f"https://api.geocod.io/v1.12/geocode?q={address}&api_key={GEOCODIO_KEY}"
geo_resp = requests.get(geo_url)
geo_resp.raise_for_status() # raise on bad status
geo_data = geo_resp.json()
if not geo_data.get('results'):
return jsonify({"error": "No location"}), 404

loc = geo_data [0]['location']
lat, lng = loc , loc fema_url = f"https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28/query?geometry={lng},{lat}&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=FLOOD_ZONE,SFHA_TF&f=json"
fema_resp = requests.get(fema_url)
fema_resp.raise_for_status()
fema_data = fema_resp.json()
features = fema_data.get('features', [ 0]['attributes' 0] == 'T'
risk = "high" if zone in or sfha else "low"
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
except Exception as e:
return jsonify({"error": str(e)}), 500

