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

router = APIRouter(prefix="/detection", tags=["detection"])

# Cloudinary will automatically look for the CLOUDINARY_URL environment variable
# Or you can configure it explicitly using the below variables if they exist
cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET")
)

@router.post("/save", response_model=schemas.DetectionSessionResponse)
async def save_detection(
    data: str = Form(..., description="JSON string containing counts and confidence"),
    video: Optional[UploadFile] = File(None, description="Optional recorded video file"),
    db: Session = Depends(database.get_db)
):
    try:
        # Parse the JSON string from the form data
        parsed_data = json.loads(data)
        detection_data = schemas.DetectionSessionCreate(**parsed_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON data: {str(e)}")

    video_url = None
    if video:
        try:
            # Upload the video buffer directly to Cloudinary
            upload_result = cloudinary.uploader.upload(
                video.file, 
                resource_type="video",
                folder="vehicle_detections"
            )
            video_url = upload_result.get("secure_url")
        except Exception as e:
            print(f"Cloudinary upload failed: {e}")
            # If Cloudinary is not properly configured, we won't crash the request,
            # but the video_url will remain None.

    db_session = models.DetectionSession(
        **detection_data.model_dump(),
        video_url=video_url
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session
