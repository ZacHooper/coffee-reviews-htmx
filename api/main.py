from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from mangum import Mangum
from utils import s3
import uuid

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

BUCKET = "coffee-review"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    coffees = s3.get_active_coffees(BUCKET)
    return templates.TemplateResponse(
        request=request, name="index.html", context={"coffees": coffees}
    )


@app.post("/api/review", response_class=HTMLResponse)
async def review(request: Request):
    # Get the form data
    form = await request.form()
    # res = s3.upload_review(dict(form), BUCKET)
    res = True
    if res:
        return templates.TemplateResponse(request=request, name="success.html")
    else:
        return templates.TemplateResponse(request=request, name="error.html")


@app.get("/api/review", response_class=HTMLResponse)
async def review(request: Request):
    return templates.TemplateResponse(request=request, name="form.html")


@app.get("/api/pantry", response_class=HTMLResponse)
async def show_pantry(request: Request):
    coffees = s3.get_active_coffees(BUCKET)
    return templates.TemplateResponse(
        request=request, name="pantry.html", context={"coffees": coffees}
    )


# no response
@app.post("/api/coffees", response_class=HTMLResponse)
async def show_pantry(request: Request):
    form = await request.form()
    active_coffees = s3.get_all_coffees(BUCKET)
    # TODO: handle coffee already exists. Ask if they want to refill instead

    form_data = dict(form)
    form_data["active"] = "True"
    form_data["id"] = str(uuid.uuid4())

    # add the new coffee to the list of active coffees
    active_coffees.append(form_data)

    s3.update_coffees(active_coffees, BUCKET)
    return templates.TemplateResponse(request=request, name="new_coffee_form.html")


@app.delete("/api/coffees/{coffee_id}", response_class=HTMLResponse)
async def show_pantry(request: Request, coffee_id: str):
    all_coffees = s3.get_all_coffees(BUCKET)
    # change the coffee to inactive
    updated_coffee = [coffee for coffee in all_coffees if coffee["uuid"] == coffee_id][
        0
    ]
    updated_coffee["active"] = False

    # update the coffee list
    all_coffees = [
        coffee if coffee["uuid"] != coffee_id else updated_coffee
        for coffee in all_coffees
    ]

    s3.update_coffees(all_coffees, BUCKET)

    # get the active coffees
    active_coffees = s3.get_active_coffees(BUCKET)
    return templates.TemplateResponse(
        request=request, name="pantry.html", context={"coffees": active_coffees}
    )


handler = Mangum(app)
