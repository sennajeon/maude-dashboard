import requests
import pandas as pd

def get_maude_data(product_code, limit=20):
    print("Calling get_maude_data with:", product_code)
    url = "https://api.fda.gov/device/event.json"
    params = {
        "search": f"device.device_report_product_code:{product_code}",
        "limit": limit,
        "sort": "date_received:desc"
    }

    # Print full request URL for debugging
    import urllib.parse
    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    print("Requesting URL:", full_url)

    r = requests.get(url, params=params)

    if r.status_code != 200:
        print("API error:", r.status_code, r.text)
        return pd.DataFrame()
    
    data = r.json()
    if "results" not in data:
        print("No results found in response.")
        return pd.DataFrame()
    
    print("Sample record:", data["results"][0])
    print("Keys in first record:", data["results"][0].keys())

    return pd.DataFrame(data["results"])

    

