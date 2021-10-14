from fastapi import FastAPI

from app.routes.routes import router
from app.db.connection import client

app = FastAPI()

app.include_router(router)

@app.get("/")
async def root():
  return {"message": "Working"}


@app.on_event("shutdown")
def shutdown_event():
    client.close()


