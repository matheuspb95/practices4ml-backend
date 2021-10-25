from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.routes import routers
from app.db.connection import client

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

for router in routers:
  app.include_router(router)

@app.get("/")
async def root():
  return {"message": "API Working"}


@app.on_event("shutdown")
def shutdown_event():
    client.close()

