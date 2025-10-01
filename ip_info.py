import requests

def get_ip_info():
    try:
        resp = requests.get("https://ipapi.co/json/", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print("Error fetching IP info:", e)
        return None

def display_info(info):
    if not info:
        print("No information available.")
        return

    print("------- IP INFORMATION -------")
    print(f"IP Address : {info.get('ip','N/A')}")
    print(f"Version    : {info.get('version','N/A')}")
    print(f"ASN        : {info.get('asn','N/A')}")
    print(f"Org / ISP  : {info.get('org','N/A')}")
    print(f"Country    : {info.get('country_name','N/A')}")
    print(f"Region     : {info.get('region','N/A')}")
    print(f"City       : {info.get('city','N/A')}")
    print(f"Latitude   : {info.get('latitude','N/A')}")
    print(f"Longitude  : {info.get('longitude','N/A')}")
    print(f"Timezone   : {info.get('timezone','N/A')}")
    print("------------------------------")

def main():
    print("Fetching current public IP & geolocation info …")
    info = get_ip_info()
    display_info(info)

if __name__ == "__main__":
    main()
