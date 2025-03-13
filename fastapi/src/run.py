import os

import uvicorn
from api.v1.endpoints import login_router, team_router, user_router
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI

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
app.include_router(user_router)
app.include_router(login_router)
app.include_router(team_router)

if __name__ == "__main__":
    uvicorn.run("run:app", host=HOST, port=int(PORT), reload=True)
