import requests

def check_fda_recalls(product_name):
    url = "https://api.fda.gov/food/enforcement.json"
    params = {
        "search": f"product_description:{product_name}",
        "limit": 3
    }
    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()
        if "results" in data:
            return {"recalls": data["results"]}
        return {"message": "No recalls found."}
    except Exception as e:
        return {"error": str(e)}
