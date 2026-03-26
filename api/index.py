from flask import Flask, request, jsonify
import requests

# TODO: Add your GEOCODIO_KEY as Environment Variable in Vercel Dashboard
# Do NOT hardcode it here for security

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Flood Risk API is running! Use /scan with address parameter."})

@app.route('/scan', methods=['GET', 'POST'])
def scan():
    try:
        # Get address from form or JSON
        if request.method == 'POST':
            address = request.form.get('address') or (request.get_json() or {}).get('address')
        else:
            address = request.args.get('address')

        if not address:
            return jsonify({"error": "No address provided"}), 400

        # Geocode using Geocodio
        geo_url = f"https://api.geocod.io/v1.12/geocode?q={address}&api_key={GEOCODIO_KEY}"
        geo_resp = requests.get(geo_url, timeout=10)
        geo_resp.raise_for_status()
        geo_data = geo_resp.json()

        if not geo_data.get('results'):
            return jsonify({"error": "No location found"}), 404

        # Extract lat/lng
        result = geo_data['results'][0]
        lat = result['location']['lat']
        lng = result['location']['lng']

        # Query FEMA flood zone
        fema_url = f"https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28/query?geometry={lng},{lat}&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=FLOOD_ZONE,SFHA_TF&f=json"
        
        fema_resp = requests.get(fema_url, timeout=10)
        fema_resp.raise_for_status()
        fema_data = fema_resp.json()

        features = fema_data.get('features', [])
        print("App starting...")  # for logs
        if features:
            attrs = features[0].get('attributes', {})
            zone = attrs.get('FLOOD_ZONE', 'Unknown')
            sfha = attrs.get('SFHA_TF', 'N') == 'T'
            
            risk = "high" if zone in ['A', 'AE', 'AO', 'AH', 'VE', 'V'] or sfha else "low"
            reason = f"Flood zone: {zone} (SFHA: {'Yes' if sfha else 'No'})"
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

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Important for Vercel
if __name__ == "__main__":
    app.run()#
