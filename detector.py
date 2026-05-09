from ultralytics import YOLO
from PIL import Image
import io
import os

# Ensure the models directory exists
os.makedirs("models", exist_ok=True)

# Load YOUR trained model instead of the default yolov8n.pt
# We are using Approach 2: Local Inference via Roboflow Weights
model_path = "models/best.pt"
if not os.path.exists(model_path):
    print(f"Warning: Model not found at {model_path}. Please run download_roboflow_model.py first.")
    # Fallback to YOLOv8n just to prevent instant crashing if the file is missing
    model = YOLO("yolov8n.pt") 
else:
    model = YOLO(model_path)

def run_detection(image_bytes: bytes) -> dict:
    image = Image.open(io.BytesIO(image_bytes))
    results = model(image)

    detections = []
    for result in results:
        for box in result.boxes:
            detections.append({
                "class": result.names[int(box.cls)],
                "confidence": round(float(box.conf), 4),
                "bbox": box.xyxy[0].tolist()
            })

    return {"detections": detections}