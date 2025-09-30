import requests
import json
import sys
from datetime import datetime

class IPAddressApp:
    def __init__(self):
        self.apis = {
            'ipapi': 'https://ipapi.co/json/',
            'ipapi_com': 'http://ip-api.com/json/',
            'ipify_v4': 'https://api.ipify.org?format=json',
            'ipify_v6': 'https://api64.ipify.org?format=json'
        }
        
    def get_ip_info(self, api_name, url):
        """Generic method to fetch IP information from different APIs"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {api_name}: {e}")
            return None
    
    def get_comprehensive_ip_info(self):
        """Get comprehensive IP information using multiple APIs"""
        print("🔍 Retrieving IP address information...")
        print("=" * 60)
        
        # Get IPv4 and IPv6 addresses
        ipv4_info = self.get_ip_info('ipify_v4', self.apis['ipify_v4'])
        ipv6_info = self.get_ip_info('ipify_v6', self.apis['ipify_v6'])
        
        # Get detailed information from ipapi.co
        detailed_info = self.get_ip_info('ipapi', self.apis['ipapi'])
        
        # Get additional information from ip-api.com
        additional_info = self.get_ip_info('ipapi_com', self.apis['ipapi_com'])
        
        # Display results
        self.display_results(ipv4_info, ipv6_info, detailed_info, additional_info)
    
    def display_results(self, ipv4_info, ipv6_info, detailed_info, additional_info):
        """Display formatted IP information"""
        
        # Basic IP addresses
        print("\n🌐 PUBLIC IP ADDRESSES:")
        print("-" * 30)
        
        if ipv4_info and 'ip' in ipv4_info:
            print(f"IPv4 Address: {ipv4_info['ip']}")
        else:
            print("IPv4 Address: Not available")
            
        if ipv6_info and 'ip' in ipv6_info:
            print(f"IPv6 Address: {ipv6_info['ip']}")
        else:
            print("IPv6 Address: Not available")
        
        # Detailed information from ipapi.co
        if detailed_info:
            print("\n📍 LOCATION INFORMATION:")
            print("-" * 30)
            print(f"City: {detailed_info.get('city', 'N/A')}")
            print(f"Region: {detailed_info.get('region', 'N/A')}")
            print(f"Country: {detailed_info.get('country_name', 'N/A')} ({detailed_info.get('country_code', 'N/A')})")
            print(f"Postal Code: {detailed_info.get('postal', 'N/A')}")
            print(f"Timezone: {detailed_info.get('timezone', 'N/A')}")
            
            print("\n🏢 NETWORK INFORMATION:")
            print("-" * 30)
            print(f"ISP: {detailed_info.get('org', 'N/A')}")
            print(f"ASN: {detailed_info.get('asn', 'N/A')}")
        
        # Additional information from ip-api.com
        if additional_info and additional_info.get('status') == 'success':
            print("\n📊 ADDITIONAL DETAILS:")
            print("-" * 30)
            print(f"ISP: {additional_info.get('isp', 'N/A')}")
            print(f"Organization: {additional_info.get('org', 'N/A')}")
            print(f"AS: {additional_info.get('as', 'N/A')}")
            print(f"Latitude: {additional_info.get('lat', 'N/A')}")
            print(f"Longitude: {additional_info.get('lon', 'N/A')}")
        
        print("\n" + "=" * 60)
        print(f"Query completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def check_specific_ip(self, ip_address):
        """Check information for a specific IP address"""
        print(f"\n🔍 Checking information for IP: {ip_address}")
        print("=" * 50)
        
        try:
            # Using ip-api.com for specific IP lookup
            url = f"http://ip-api.com/json/{ip_address}"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data.get('status') == 'success':
                print(f"Country: {data.get('country', 'N/A')}")
                print(f"Region: {data.get('regionName', 'N/A')}")
                print(f"City: {data.get('city', 'N/A')}")
                print(f"ISP: {data.get('isp', 'N/A')}")
                print(f"Organization: {data.get('org', 'N/A')}")
                print(f"AS: {data.get('as', 'N/A')}")
                print(f"Latitude: {data.get('lat', 'N/A')}")
                print(f"Longitude: {data.get('lon', 'N/A')}")
                print(f"Timezone: {data.get('timezone', 'N/A')}")
            else:
                print("Error: Could not retrieve information for the specified IP")
                
        except requests.exceptions.RequestException as e:
            print(f"Error checking IP {ip_address}: {e}")

def main():
    app = IPAddressApp()
    
    print("🚀 IP Address Information Application")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Get my current IP information")
        print("2. Check specific IP address")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            app.get_comprehensive_ip_info()
        elif choice == '2':
            ip_address = input("Enter IP address to check: ").strip()
            if ip_address:
                app.check_specific_ip(ip_address)
            else:
                print("Please enter a valid IP address")
        elif choice == '3':
            print("Thank you for using the IP Address Application!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # Check if requests library is installed
    try:
        import requests
    except ImportError:
        print("Error: The 'requests' library is required but not installed.")
        print("Please install it using: pip install requests")
        sys.exit(1)
    
    main()