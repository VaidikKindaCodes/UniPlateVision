# UniPlate Vision Backend

Small FastAPI service for demonstrating license-plate detection with an
Ultralytics YOLO model.

## Run locally

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r Backend\requirements.txt
$env:MODEL_PATH = "C:\path\to\best.pt"
uvicorn Backend.app.main:app --reload
```

If the model is stored at `Backend\models\best.pt`, `MODEL_PATH` is optional.
The repository currently does not include trained weights.

## Endpoints

- `GET /health` reports whether model weights are available.
- `POST /predict` accepts an image upload in the `file` field. An optional
  `confidence` query parameter controls the detection threshold.
- `GET /docs` opens the interactive Swagger UI.

Example:

```powershell
curl.exe -X POST "http://127.0.0.1:8000/predict?confidence=0.25" `
  -F "file=@Dataset\Dataset\some-image.jpg"
```

The prediction response contains the detected class, confidence, and
`[x1, y1, x2, y2]` pixel coordinates for every plate.
