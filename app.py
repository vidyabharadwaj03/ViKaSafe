from fastapi import FastAPI
from recall_checker import check_fda_recalls

app = FastAPI()

@app.get("/")
def root():
    return {"message": "ViKa Recall Checker API is running"}

@app.get("/recall/{product_name}")
def recall_status(product_name: str):
    return check_fda_recalls(product_name)
