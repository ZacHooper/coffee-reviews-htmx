from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from mangum import Mangum

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


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
    print(form)
    return templates.TemplateResponse(request=request, name="success.html")


@app.get("/api/review", response_class=HTMLResponse)
async def review(request: Request):
    return templates.TemplateResponse(request=request, name="form.html")


handler = Mangum(app)
