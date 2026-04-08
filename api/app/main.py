from fastapi import FastAPI
from api.app.routes import secure

app = FastAPI(
    title="Fuel Insights API",
    version="0.1.0"
)

# Load routes
app.include_router(secure.router)

@app.get("/")
def root():
    return {"status": "Fuel Insights API running"}
