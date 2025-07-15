import secrets
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

url_database = {}

def generate_short_url():
    return secrets.token_urlsafe(5)

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/shorten", response_class=HTMLResponse)
def shorten_url(request: Request, long_url: str = Form(...)):
    short_url = generate_short_url()
    url_database[short_url] = long_url
    return templates.TemplateResponse("index.html", {"request": request, "short_url": short_url})

@app.get("/{short_url}")
def redirect_to_long_url(short_url: str):
    long_url = url_database.get(short_url)
    if long_url:
        return RedirectResponse(url=long_url)
    else:
        raise HTTPException(status_code=404, detail="URL not found")
