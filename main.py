from fastapi import FastAPI

app = FastAPI(title="Investment Tracker")

@app.get("/")
def read_root():
    return {"status": "ok"}
