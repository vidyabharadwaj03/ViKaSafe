import requests

# def check_fda_recalls(product_name):
#     url = "https://api.fda.gov/food/enforcement.json"
#     params = {
#         "search": f"product_description:{product_name}",
#         "limit": 3
#     }
#     try:
#         res = requests.get(url, params=params)
#         res.raise_for_status()
#         data = res.json()
#         if "results" in data:
#             return {"recalls": data["results"]}
#         return {"message": "No recalls found."}
#     except Exception as e:
#         return {"error": str(e)}

def check_fda_recalls(product_name, brand_name=None):
    endpoint = "https://api.fda.gov/food/enforcement.json"
    params = {
        "search": f"product_description:{product_name}",
        "limit": 10
    }
    try:
        res = requests.get(endpoint, params=params)
        res.raise_for_status()
        data = res.json()
        filtered = []
        if "results" in data:
            for r in data["results"]:
                desc = r.get("product_description", "").lower()
                if product_name.lower() in desc or (brand_name and brand_name.lower() in desc):
                    filtered.append(r)
            return {"recalls": filtered} if filtered else {"message": "No matching recalls found."}
        return {"message": "No recalls found."}
    except Exception as e:
        return {"error": str(e)}

def check_cpsc_recalls(product_name):
    url = "https://www.saferproducts.gov/RestWebServices/Recall"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        matches = []

        for recall in data:
            recall_text = (recall.get("Title", "") + " " + recall.get("Description", "")).lower()
            if product_name.lower() in recall_text:
                matches.append({
                    "title": recall.get("Title"),
                    "description": recall.get("Description"),
                    "recall_number": recall.get("RecallNumber"),
                    "hazard": recall.get("Hazard"),
                    "remedy": recall.get("Remedy"),
                    "url": recall.get("URL"),
                    "recall_date": recall.get("RecallDate")
                })

        return {"recalls": matches} if matches else {"message": "No matching CPSC recalls found."}
    except Exception as e:
        return {"error": str(e)}


from pyzbar.pyzbar import decode
from PIL import Image

def extract_barcode(image: Image.Image):
    barcodes = decode(image)
    if barcodes:
        return barcodes[0].data.decode("utf-8")
    return None


def lookup_product_info(upc):
    url = f"https://api.upcitemdb.com/prod/trial/lookup?upc={upc}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("items"):
            item = data["items"][0]
            return {
                "title": item.get("title"),
                "brand": item.get("brand"),
                "description": item.get("description")
            }
        return {"error": "No product found"}
    except Exception as e:
        return {"error": str(e)}
