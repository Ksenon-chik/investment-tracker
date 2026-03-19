from fastapi import FastAPI
from routers import auth
from routers import deals
from db.init_db import init_db

app = FastAPI(title="Investment Tracker")

init_db()

app.include_router(auth.router)
app.include_router(deals.router)

@app.get("/")
def read_root():
    return {"status": "ok"}
