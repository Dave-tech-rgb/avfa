from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import Optional
import json
import cloudinary
import cloudinary.uploader
import os
from datetime import datetime

import models
import schemas
import database
from detector import run_detection  # ← add this

router = APIRouter(prefix="/detection", tags=["detection"])

cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET")
)

# ─────────────────────────────────────────────
# NEW: Run YOLOv8 on an uploaded image/frame
# ─────────────────────────────────────────────
@router.post("/detect")
async def detect(
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db)
):
    image_bytes = await file.read()
    result = run_detection(image_bytes)

    # Save each detection box to DetectionLog
    for det in result["detections"]:
        log = models.DetectionLog(
            label=det["class"],
            confidence=det["confidence"],
            bbox_x1=det["bbox"][0],
            bbox_y1=det["bbox"][1],
            bbox_x2=det["bbox"][2],
            bbox_y2=det["bbox"][3],
        )
        db.add(log)
    db.commit()

    return result


# ─────────────────────────────────────────────
# EXISTING: Save a completed detection session
# ─────────────────────────────────────────────
@router.post("/save", response_model=schemas.DetectionSessionResponse)
async def save_detection(
    data: str = Form(..., description="JSON string containing counts and confidence"),
    video: Optional[UploadFile] = File(None, description="Optional recorded video file"),
    db: Session = Depends(database.get_db)
):
    try:
        parsed_data = json.loads(data)
        detection_data = schemas.DetectionSessionCreate(**parsed_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON data: {str(e)}")

    video_url = None
    if video:
        try:
            upload_result = cloudinary.uploader.upload(
                video.file,
                resource_type="video",
                folder="vehicle_detections"
            )
            video_url = upload_result.get("secure_url")
        except Exception as e:
            print(f"Cloudinary upload failed: {e}")

    db_session = models.DetectionSession(
        **detection_data.model_dump(),
        video_url=video_url
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session