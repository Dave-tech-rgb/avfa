from ultralytics import YOLO
from PIL import Image
import io

# Load YOUR trained model instead of the default yolov8n.pt
model = YOLO("models/best.pt")

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