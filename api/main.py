from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from mangum import Mangum
from utils import s3

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

BUCKET = "coffee-review"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    id = "123"
    return templates.TemplateResponse(
        request=request, name="index.html", context={"id": id}
    )


@app.post("/api/review", response_class=HTMLResponse)
async def review(request: Request):
    # Get the form data
    form = await request.form()
    res = s3.upload_review(dict(form), BUCKET)
    if res:
        return templates.TemplateResponse(request=request, name="success.html")
    else:
        return templates.TemplateResponse(request=request, name="error.html")


@app.get("/api/review", response_class=HTMLResponse)
async def review(request: Request):
    return templates.TemplateResponse(request=request, name="form.html")


handler = Mangum(app)
