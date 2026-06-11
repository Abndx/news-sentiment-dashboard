import urllib.request
import json

print("Fetching the latest AWS Layer ARN from Klayers...")
url = "https://api.klayers.cloud/api/v2/p3.11/layers/latest/ap-south-1"

try:
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode())
    
    found = False
    for layer in data:
        # Check if the layer contains the psycopg2 package
        packages = layer.get("packages", [])
        if packages and packages[0].get("name") == "psycopg2-binary":
            print("\n✅ SUCCESS! COPY THIS EXACT ARN:")
            print("-" * 50)
            print(layer["arn"])
            print("-" * 50)
            found = True
            break
            
    if not found:
        print("Could not find the package in the current region.")
        
except Exception as e:
    print(f"Error connecting to Klayers API: {e}")