from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(
    prefix="/api/medical-records",
    tags=["Pneumonia Prediction"]
)

class PredictionResponseData(BaseModel):
    is_pneumonia: bool
    confidence: float
    heatmap_image_url: str

class PredictionResponse(BaseModel):
    success: bool
    data: PredictionResponseData

@router.post("/{record_id}/predict-pneumonia", response_model=PredictionResponse)
async def create_pneumonia_prediction(record_id: str):
    try:
        is_pneumonia = True
        confidence = 0.95
        heatmap_url = "https://example.com/images/heatmap_123.png"

        return {
            "success": True,
            "data": {
                "is_pneumonia": is_pneumonia,
                "confidence": confidence,
                "heatmap_image_url": heatmap_url
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{record_id}/pneumonia-results")
async def get_pneumonia_predictions(record_id: str):
    return [
        {
            "id": "pred_001",
            "is_pneumonia": True,
            "confidence": 0.95,
            "heatmap_image_url": "https://example.com/images/heatmap_123.png",
            "created_at": "2026-07-22T10:00:00Z",
            "model_name": "PneumoniaModel_v1"
        }
    ]
