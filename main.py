import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from app.api.api import api_router
from app.core.settings import Settings

app = FastAPI()


app.include_router(api_router)

settings = Settings()

@app.get("/")
def read_root():
    return {"Project Name": settings.PROJECT_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



