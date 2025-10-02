from flask import Flask, render_template, request
import requests, os
from dotenv import load_dotenv

app = Flask(__name__)

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("IPGEO_KEY")

def get_ip_info(ip=None):
    try:
        base_url = "https://api.ipgeolocation.io/ipgeo"
        params = {"apiKey": API_KEY}
        
        if ip and ip.strip():  # Only add IP if provided and not empty
            params["ip"] = ip.strip()
            
        resp = requests.get(base_url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

@app.route("/", methods=["GET", "POST"])
def home():
    info = None
    searched_ip = ""
    
    if request.method == "POST":
        searched_ip = request.form.get("ip_address", "").strip()
        info = get_ip_info(searched_ip if searched_ip else None)
    
    return render_template("index.html", info=info, searched_ip=searched_ip)

if __name__ == "__main__":
    app.run(debug=True)