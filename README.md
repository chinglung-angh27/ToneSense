# ToneSense — AI Facial Color Analysis

> Discover your perfect seasonal color palette using AI-powered facial analysis.

![ToneSense](https://img.shields.io/badge/ToneSense-AI%20Color%20Analysis-eb4488)

## Features

- **Live Camera or Photo Upload** — Analyze your skin tone via webcam or uploaded image
- **MediaPipe Face Mesh** — Precise facial landmark detection across forehead, cheeks, jawline, and neck
- **Color Science** — RGB → LAB conversion, undertone classification, contrast & depth analysis
- **12 Seasonal Palettes** — Light/True/Deep Spring, Light/True/Soft Summer, Soft/True/Deep Autumn, Light/True/Deep Winter
- **Complete Style Guide** — Clothing colors, jewelry tone, hair color suggestions, makeup palette
- **Downloadable Result Card** — Export your analysis as a shareable PNG
- **Dark Mode** — Full dark/light theme support
- **Privacy-First** — No images stored; processing happens on-demand only

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite + Tailwind CSS |
| Backend | Python FastAPI |
| AI/ML | MediaPipe Face Mesh + OpenCV |
| Export | html-to-image |
| Deployment | Docker + Docker Compose (Vercel/Render compatible) |

## Project Structure

```
ToneSense/
├── backend/
│   ├── analysis/
│   │   ├── face_detection.py    # MediaPipe face mesh + region masks
│   │   ├── color_extraction.py  # Skin color sampling & LAB conversion
│   │   ├── tone_classifier.py   # Undertone, depth, contrast
│   │   └── seasonal_palette.py  # 12-season classification + recommendations
│   ├── main.py                  # FastAPI server
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── hooks/               # useDarkMode
│   │   ├── utils/               # API client
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── tailwind.config.js
│   ├── vite.config.js
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.10+ with pip
- Node.js 18+ with npm
- (Optional) Docker & Docker Compose

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) — the Vite dev server proxies `/api` requests to the backend at port 8000.

### Docker (Full Stack)

```bash
docker-compose up --build
```

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend API: [http://localhost:8000/docs](http://localhost:8000/docs)

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/analyze` | Analyze uploaded image (multipart form) |
| POST | `/api/analyze-base64` | Analyze base64 image (JSON body) |

### Example Response

```json
{
  "success": true,
  "analysis": {
    "skin_color": { "rgb": [198, 168, 140], "lab": [178, 133, 149], "hex": "#c6a88c" },
    "undertone": { "classification": "warm", "warm_score": 0.72, "explanation": "..." },
    "depth": { "level": "medium", "l_value": 69.8 },
    "contrast": { "level": "medium", "chroma": 58 },
    "season": "True Autumn",
    "best_colors": ["#B8860B", "#D2691E", ...],
    "worst_colors": ["#FF69B4", "#E6E6FA", ...],
    "clothing_suggestions": [...],
    "jewelry_tone": "Rich yellow gold, antique gold...",
    "hair_color_suggestions": [...],
    "makeup_palette": { "foundation": "...", "blush": "...", ... }
  },
  "preview": "data:image/jpeg;base64,..."
}
```

## Privacy

- Images are **never stored** unless the user explicitly opts in
- Camera access requires explicit consent via a modal dialog
- All processing is done server-side in memory, with no disk persistence
- Images are discarded immediately after analysis

## License

MIT
