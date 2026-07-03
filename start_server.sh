#!/bin/bash
#
# MemeTide Server Starter
# Runs FastAPI server in production mode
#

cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Run 'python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt' first."
    exit 1
fi

# Activate venv
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "❌ Dependencies not installed. Run 'pip install -r requirements.txt' first."
    exit 1
fi

# Start server
echo ""
echo "============================================================"
echo "🌊 MEMETIDE API SERVER"
echo "============================================================"
echo "Starting FastAPI server..."
echo ""
echo "📡 Server URL:  http://localhost:8000"
echo "📚 API Docs:    http://localhost:8000/docs"
echo "📖 ReDoc:       http://localhost:8000/redoc"
echo ""
echo "============================================================"
echo ""

# Run with uvicorn directly for better control
uvicorn api_server:app \
    --host 0.0.0.0 \
    --port 8000 \
    --log-level info \
    --reload
