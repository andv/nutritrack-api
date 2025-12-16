from fastapi import FastAPI
from app.parsers.calorizator import fetch_product_data

app = FastAPI(title="NutriTrack API")

@app.get("/search")
async def search_product(q: str):
    try:
        results = fetch_product_data(q)
        return {"query": q, "results": results}
    except Exception as e:
        return {"error": str(e)}, 400
