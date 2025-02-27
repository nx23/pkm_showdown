import uvicorn
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.endpoints.users import router as user_router #type: ignore

load_dotenv()

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

if HOST is None:
    raise ValueError("HOST environment variable is not set")

if PORT is None:
    raise ValueError("PORT environment variable is not set")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router
app.include_router(user_router, prefix="/api/v1")

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

if __name__ == "__main__":
    uvicorn.run("run:app", host=HOST, port=int(PORT), reload=False)