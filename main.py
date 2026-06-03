from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routers import auth, deals, analytics, profile
from db.init_db import init_db
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Investment Tracker")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    err = exc.errors()[0]
    msg = err.get("msg")
    clean_msg = msg.split("Value error, ")[-1]
    
    if "greater than or equal to 0" in clean_msg.lower():
        clean_msg = "Начальный баланс должен быть больше или равен 0"

    if "field required" in clean_msg.lower():
        field = err.get("loc")[-1]
        fields = {"email": "Email", "password": "Пароль", "start_balance": "Начальный баланс"}
        clean_msg = f"Поле {fields.get(field, field)} обязательно"
    
    return JSONResponse(
        status_code=422,
        content={"detail": clean_msg},
    )

init_db()

app.include_router(auth.router)
app.include_router(deals.router)
app.include_router(analytics.router)
app.include_router(profile.router)

templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/auth-page")
def auth_page(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})