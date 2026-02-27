#!/usr/bin/env bash
# build.sh — build frontend and copy into backend/static for unified deployment
set -e

echo "→ Building React frontend..."
cd "$(dirname "$0")/frontend"
npm install
npm run build

echo "→ Copying dist/ to backend/static/..."
cd ..
rm -rf backend/static
cp -r frontend/dist backend/static

echo "✓ Done. Run: cd backend && uvicorn main:app --host 0.0.0.0 --port 8000"
