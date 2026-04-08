from fastapi import APIRouter, Depends
from api.core.auth import require_role

router = APIRouter()

@router.get("/fuel/history")
def get_history(user=Depends(require_role("viewer"))):
    return {"message": "Fuel history visible", "user": user}

@router.post("/fuel/admin/ingest")
def ingest_data(user=Depends(require_role("admin"))):
    return {"message": "Data ingested", "user": user}
