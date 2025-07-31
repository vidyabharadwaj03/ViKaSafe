from fastapi import FastAPI
from recall_checker import check_fda_recalls

app = FastAPI()

@app.get("/")
def root():
    return {"message": "ViKa Recall Checker API is running"}

@app.get("/recall/{product_name}")
def recall_status(product_name: str):
    return check_fda_recalls(product_name)


from fastapi import FastAPI, File, UploadFile
from recall_checker import check_fda_recalls, extract_barcode
from fastapi.responses import JSONResponse
from PIL import Image
import io

app = FastAPI()

# @app.post("/scan-barcode/")
# async def scan_barcode(file: UploadFile = File(...)):
#     contents = await file.read()
#     image = Image.open(io.BytesIO(contents))
#     upc = extract_barcode(image)
#     if not upc:
#         return JSONResponse(content={"error": "No barcode detected"}, status_code=404)
#     return {"upc": upc}

# from recall_checker import extract_barcode, lookup_product_info

# @app.post("/scan-barcode/")
# async def scan_barcode(file: UploadFile = File(...)):
#     contents = await file.read()
#     image = Image.open(io.BytesIO(contents))
#     upc = extract_barcode(image)
#     if not upc:
#         return JSONResponse(content={"error": "No barcode detected"}, status_code=404)

#     product_info = lookup_product_info(upc)
#     return {
#         "upc": upc,
#         "product_info": product_info
#     }

from recall_checker import extract_barcode, lookup_product_info, check_fda_recalls
from recall_checker import check_cpsc_recalls

@app.post("/scan-barcode/")
async def scan_barcode(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    upc = extract_barcode(image)
    if not upc:
        return JSONResponse(content={"error": "No barcode detected"}, status_code=404)

    product_info = lookup_product_info(upc)
    title = product_info.get("title", "")
    brand = product_info.get("brand", "")

    # ✅ Updated line with brand filtering
    recall_data = check_fda_recalls(title, brand)
    # ...inside your scan_barcode endpoint
    cpsc_data = check_cpsc_recalls(title)

    

    return {
    "upc": upc,
    "product_info": product_info,
    "recall_check_fda": recall_data,
    "recall_check_cpsc": cpsc_data
    }





