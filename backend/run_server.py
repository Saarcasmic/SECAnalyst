import uvicorn
import os

if __name__ == "__main__":
    # Ensure environment is loaded or rely on system env
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
