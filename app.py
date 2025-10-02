from flask import Flask, render_template, request
import requests, os
from dotenv import load_dotenv

app = Flask(__name__)

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("IPGEO_KEY")  # <-- rename to match your new provider (optional)

def get_ip_info(ip=None):
    try:
        base_url = "https://api.ipgeolocation.io/ipgeo"
        if ip:
            url = f"{base_url}?apiKey={API_KEY}&ip={ip}"
        else:
            url = f"{base_url}?apiKey={API_KEY}"

        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

@app.route("/", methods=["GET", "POST"])
def home():
    ip = None
    if request.method == "POST":
        ip = request.form.get("ip_address")
    info = get_ip_info(ip)
    return render_template("index.html", info=info, searched_ip=ip)

if __name__ == "__main__":
    app.run(debug=True)
