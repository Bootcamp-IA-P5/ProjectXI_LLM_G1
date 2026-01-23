#!/usr/bin/env python
"""
Entry point for running the FastAPI application.
This script should be run from the project root.
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get port from environment variable or command line argument
    port = int(os.getenv("SERVER_PORT", "5001"))
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    
    # Run Uvicorn server
    uvicorn.run(
        "app:app",
        host=os.getenv("SERVER_HOST", "0.0.0.0"),
        port=port,
        reload=True,
        log_level="info"
    )
