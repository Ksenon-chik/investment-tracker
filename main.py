from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from routers import auth, deals, analytics, profile
from db.init_db import init_db
from db.session import get_db
from fastapi.responses import HTMLResponse, RedirectResponse
from services.user_service import get_user_by_id
from sqlalchemy.orm import Session
from utils.calculations import calculate_total_capital, equity_curve

templates = Jinja2Templates(directory="templates")

app = FastAPI(title="Investment Tracker")

init_db()

app.include_router(auth.router)
app.include_router(deals.router)
app.include_router(analytics.router)
app.include_router(profile.router)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/auth-page")
def auth_page(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})
