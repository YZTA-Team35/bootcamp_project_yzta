from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/public/static"), name="static")
templates = Jinja2Templates(directory="app/public/templates")

@app.get("/", response_class=HTMLResponse) # home ekranı
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/signin", response_class=HTMLResponse) # signin ekranı
def signin_get(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse) # signup ekranı
def signup_get(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse) # chat assistan
def chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})
