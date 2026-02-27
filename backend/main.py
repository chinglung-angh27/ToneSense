"""
ToneSense API — FastAPI backend for AI-based facial color analysis.
"""

import io
import base64
import logging
from contextlib import asynccontextmanager
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from analysis.face_detection import FaceDetector
from analysis.color_extraction import ColorExtractor
from analysis.tone_classifier import ToneClassifier
from analysis.seasonal_palette import SeasonalPaletteClassifier

logger = logging.getLogger("tonesense")

STATIC_DIR = Path(__file__).parent / "static"

# ── Shared singleton instances ────────────────────────────────
face_detector: FaceDetector | None = None
color_extractor = ColorExtractor()
tone_classifier = ToneClassifier()
palette_classifier = SeasonalPaletteClassifier()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    global face_detector
    logger.info("Initialising MediaPipe Face Mesh …")
    face_detector = FaceDetector()
    yield
    if face_detector:
        face_detector.close()
    logger.info("Shut down cleanly.")


app = FastAPI(
    title="ToneSense API",
    description="AI-powered facial color analysis and seasonal palette classification",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Helpers ───────────────────────────────────────────────────

def _read_image(data: bytes) -> np.ndarray:
    """Decode raw bytes into a BGR numpy image."""
    arr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode image")
    return img


def _create_annotated_preview(image: np.ndarray, face_data: dict) -> str:
    """Draw detected regions on the image and return a base64 JPEG."""
    preview = image.copy()
    colors = {
        "forehead": (255, 182, 193),
        "left_cheek": (173, 216, 230),
        "right_cheek": (173, 216, 230),
        "jawline": (144, 238, 144),
        "neck": (255, 218, 185),
    }
    for region_name, mask in face_data["regions"].items():
        color = colors.get(region_name, (200, 200, 200))
        overlay = preview.copy()
        overlay[mask > 0] = color
        cv2.addWeighted(overlay, 0.3, preview, 0.7, 0, preview)

    # Encode to base64
    _, buf = cv2.imencode(".jpg", preview, [cv2.IMWRITE_JPEG_QUALITY, 85])
    b64 = base64.b64encode(buf.tobytes()).decode("utf-8")
    return f"data:image/jpeg;base64,{b64}"


# ── Routes ────────────────────────────────────────────────────

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "ToneSense API"}


@app.post("/api/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyze an uploaded face image.

    Accepts JPEG / PNG.  Returns full analysis with seasonal palette,
    undertone, contrast, depth, and style recommendations.
    """
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload a valid image file")

    data = await file.read()
    if len(data) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image must be under 10 MB")

    try:
        image = _read_image(data)
    except ValueError:
        raise HTTPException(status_code=400, detail="Could not decode image")

    # Limit resolution for performance
    max_dim = 1280
    h, w = image.shape[:2]
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        image = cv2.resize(image, (int(w * scale), int(h * scale)))

    # 1. Face detection
    face_data = face_detector.detect(image)
    if face_data is None:
        raise HTTPException(
            status_code=422,
            detail="No face detected. Please upload a clear, well-lit photo with your face visible.",
        )

    # 2. Color extraction
    color_data = color_extractor.extract(
        image, face_data["regions"], face_data["face_mask"]
    )
    if "error" in color_data:
        raise HTTPException(status_code=422, detail=color_data["error"])

    # 3. Tone classification
    tone_data = tone_classifier.classify(color_data)

    # 4. Seasonal palette
    palette_result = palette_classifier.classify(tone_data, color_data)

    # 5. Annotated preview
    preview_b64 = _create_annotated_preview(image, face_data)

    return JSONResponse(
        content={
            "success": True,
            "analysis": {
                "skin_color": color_data["overall"],
                "regions": color_data["regions"],
                "undertone": tone_data["undertone"],
                "depth": tone_data["depth"],
                "contrast": tone_data["contrast"],
                "season": palette_result["season"],
                "season_description": palette_result["description"],
                "best_colors": palette_result["best_colors"],
                "worst_colors": palette_result["worst_colors"],
                "clothing_suggestions": palette_result["clothing_suggestions"],
                "jewelry_tone": palette_result["jewelry_tone"],
                "hair_color_suggestions": palette_result["hair_color_suggestions"],
                "makeup_palette": palette_result["makeup_palette"],
            },
            "preview": preview_b64,
        }
    )


@app.post("/api/analyze-base64")
async def analyze_base64(body: dict):
    """
    Analyze a base64-encoded image (for live camera frames).
    Body: { "image": "data:image/jpeg;base64,..." }
    """
    image_data = body.get("image", "")
    if not image_data:
        raise HTTPException(status_code=400, detail="No image data provided")

    # Strip data URI prefix
    if "," in image_data:
        image_data = image_data.split(",", 1)[1]

    try:
        raw = base64.b64decode(image_data)
        image = _read_image(raw)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 image data")

    # Limit resolution
    max_dim = 1280
    h, w = image.shape[:2]
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        image = cv2.resize(image, (int(w * scale), int(h * scale)))

    face_data = face_detector.detect(image)
    if face_data is None:
        raise HTTPException(status_code=422, detail="No face detected in frame.")

    color_data = color_extractor.extract(
        image, face_data["regions"], face_data["face_mask"]
    )
    if "error" in color_data:
        raise HTTPException(status_code=422, detail=color_data["error"])

    tone_data = tone_classifier.classify(color_data)
    palette_result = palette_classifier.classify(tone_data, color_data)
    preview_b64 = _create_annotated_preview(image, face_data)

    return JSONResponse(
        content={
            "success": True,
            "analysis": {
                "skin_color": color_data["overall"],
                "regions": color_data["regions"],
                "undertone": tone_data["undertone"],
                "depth": tone_data["depth"],
                "contrast": tone_data["contrast"],
                "season": palette_result["season"],
                "season_description": palette_result["description"],
                "best_colors": palette_result["best_colors"],
                "worst_colors": palette_result["worst_colors"],
                "clothing_suggestions": palette_result["clothing_suggestions"],
                "jewelry_tone": palette_result["jewelry_tone"],
                "hair_color_suggestions": palette_result["hair_color_suggestions"],
                "makeup_palette": palette_result["makeup_palette"],
            },
            "preview": preview_b64,
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


# ── Serve React frontend (must be registered LAST) ────────────
# Only mount if the static folder exists (i.e. after `npm run build`)
if STATIC_DIR.exists():
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        """Catch-all: return index.html for any non-API route (SPA routing)."""
        index = STATIC_DIR / "index.html"
        if index.exists():
            return FileResponse(index)
        return JSONResponse({"error": "Frontend not built. Run: npm run build"}, status_code=404)
