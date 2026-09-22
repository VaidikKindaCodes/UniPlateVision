from io import BytesIO
import os
from pathlib import Path
from threading import Lock
from typing import Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError


BACKEND_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = Path(
    os.getenv("MODEL_PATH", str(BACKEND_DIR / "models" / "best.pt"))
)
MAX_UPLOAD_BYTES = 10 * 1024 * 1024

app = FastAPI(
    title="UniPlate Vision ANPR API",
    description="Minimal license-plate detection backend.",
    version="0.1.0",
)

_model: Any = None
_model_lock = Lock()


def get_model() -> Any:
    """Load the detector once, only when the first prediction is requested."""
    global _model
    if _model is not None:
        return _model

    if not MODEL_PATH.is_file():
        raise HTTPException(
            status_code=503,
            detail=(
                "Model weights are not configured. Set MODEL_PATH to a trained "
                f"Ultralytics .pt file (looked for {MODEL_PATH})."
            ),
        )

    with _model_lock:
        if _model is None:
            try:
                from ultralytics import YOLO

                _model = YOLO(str(MODEL_PATH))
            except Exception as exc:
                raise HTTPException(
                    status_code=503,
                    detail=f"Could not load model weights: {exc}",
                ) from exc
    return _model


@app.get("/health")
def health() -> dict[str, object]:
    return {
        "status": "ok",
        "model_configured": MODEL_PATH.is_file(),
        "model_path": str(MODEL_PATH),
    }


@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    confidence: float = 0.25,
) -> dict[str, object]:
    if not 0 <= confidence <= 1:
        raise HTTPException(
            status_code=422, detail="confidence must be between 0 and 1"
        )
    if file.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(
            status_code=415,
            detail="Only JPEG, PNG, and WebP images are supported",
        )

    contents = await file.read()
    if len(contents) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Image must be 10 MB or smaller")

    try:
        image = Image.open(BytesIO(contents)).convert("RGB")
    except (UnidentifiedImageError, OSError) as exc:
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid image") from exc

    model = get_model()
    try:
        result = model(image, conf=confidence, verbose=False)[0]
        names = result.names
        detections = []
        if result.boxes is not None:
            for box in result.boxes:
                class_id = int(box.cls.item())
                detections.append(
                    {
                        "label": names[class_id],
                        "confidence": round(float(box.conf.item()), 4),
                        "box": [round(float(value), 2) for value in box.xyxy[0].tolist()],
                    }
                )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc

    return {
        "filename": file.filename,
        "image_size": {"width": image.width, "height": image.height},
        "detections": detections,
    }
