# ── Stage 1: Build React frontend ────────────────────────────
FROM node:20-alpine AS frontend-build

WORKDIR /frontend
COPY ../frontend/package.json ./
RUN npm install
COPY ../frontend/ .
RUN npm run build

# ── Stage 2: Python backend + bundled frontend ────────────────
FROM python:3.11-slim

WORKDIR /app

# System deps for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Copy built frontend into backend/static
COPY --from=frontend-build /frontend/dist ./static

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
