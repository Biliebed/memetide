#!/bin/bash
# Railway startup script with NLTK data download

echo "🌊 MemeTide Starting..."

# Download NLTK data if not exists
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('brown', quiet=True); nltk.download('punkt_tab', quiet=True)"

echo "✅ NLTK data ready"

# Start server with proper PORT handling
PORT=${PORT:-8000}
echo "🚀 Starting Uvicorn on port $PORT..."
uvicorn api_server:app --host 0.0.0.0 --port $PORT
