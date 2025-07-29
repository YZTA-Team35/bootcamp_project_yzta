from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse) #home ekranı
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/signin", response_class=HTMLResponse) # signin ekranı
async def signin_get(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse) # chat assistan
async def chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})
