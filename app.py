from flask import Flask, render_template, request
import requests, os
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
            ip_list = text_area_ips.split("\n")
            batch_results = batch_lookup(ip_list)

    return render_template(
        "index.html",
        info=info,
        searched_ip=searched_ip,
        batch_results=batch_results
    )


if __name__ == "__main__":
    app.run(debug=True)
