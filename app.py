from flask import Flask, render_template
import requests

app = Flask(__name__)

def get_ip_info():
    try:
        resp = requests.get("https://ipapi.co/json/", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def home():
    info = get_ip_info()
    return render_template("index.html", info=info)

if __name__ == "__main__":
    app.run(debug=True)
