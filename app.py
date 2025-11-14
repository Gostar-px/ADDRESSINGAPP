from flask import Flask, render_template, request, jsonify
import requests, os, csv
from io import StringIO
from dotenv import load_dotenv

app = Flask(__name__)

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("IPGEO_KEY")

def get_ip_info(ip=None):
    try:
        base_url = "https://api.ipgeolocation.io/ipgeo"
        params = {"apiKey": API_KEY}

        if ip and ip.strip():
            params["ip"] = ip.strip()

        resp = requests.get(base_url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

# ✅ BATCH LOOKUP FUNCTION (NEW)
def batch_lookup(ip_list):
    results = []
    for ip in ip_list:
        ip = ip.strip()
        if ip:
            results.append({
                "ip": ip,
                "result": get_ip_info(ip)
            })
    return results

# ✅ NEW API ENDPOINT FOR BATCH LOOKUP
@app.route("/api/lookup", methods=["GET"])
def api_lookup():
    ip = request.args.get("ip", "").strip()
    if not ip:
        return jsonify({"error": "IP address is required"}), 400
    
    result = get_ip_info(ip)
    return jsonify(result)

# 🟦 MAIN ROUTE UPDATED — handles single + batch lookup
@app.route("/", methods=["GET", "POST"])
def home():
    info = None
    searched_ip = ""
    batch_results = None

    if request.method == "POST":
        mode = request.form.get("mode")

        # ---------------- SINGLE LOOKUP ----------------
        if mode == "single":
            searched_ip = request.form.get("ip_address", "").strip()
            info = get_ip_info(searched_ip if searched_ip else None)

        # ---------------- BATCH LOOKUP (NEW) ----------------
        elif mode == "batch":
            text_area_ips = request.form.get("batch_ips", "")
            ip_list = [ip.strip() for ip in text_area_ips.replace(',', '\n').split('\n') if ip.strip()]
            batch_results = batch_lookup(ip_list)

    return render_template(
        "index.html",
        info=info,
        searched_ip=searched_ip,
        batch_results=batch_results
    )

# ✅ CSV DOWNLOAD ENDPOINT
@app.route("/download-csv", methods=["POST"])
def download_csv():
    try:
        data = request.get_json()
        if not data or "results" not in data:
            return jsonify({"error": "No data provided"}), 400
        
        # Create CSV in memory
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(["IP Address", "Country", "Region", "City", "ISP", "Organization", "Latitude", "Longitude"])
        
        # Write data
        for result in data["results"]:
            ip = result["ip"]
            data = result["data"]
            
            writer.writerow([
                ip,
                data.get("country_name", "") or data.get("country", ""),
                data.get("state_prov", "") or data.get("region", ""),
                data.get("city", ""),
                data.get("isp", ""),
                data.get("organization", ""),
                data.get("latitude", ""),
                data.get("longitude", "")
            ])
        
        # Return CSV file
        output.seek(0)
        return output.getvalue(), 200, {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename="ip_lookup_results.csv"'
        }
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)