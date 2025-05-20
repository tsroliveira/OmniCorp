import uvicorn
import os

if __name__ == "__main__":
    uvicorn.run(
        "app.backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 