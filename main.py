from fastapi import FastAPI
from core import services, models
from config import configure_app

app = FastAPI()
configure_app(app)


@app.post("/about-me")
async def about_me(user: models.User):
    response = services.about_me(user)
    return {"message": "success", "data": response}
