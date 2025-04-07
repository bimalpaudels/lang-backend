from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from starlette import status

from core import services, models
from config import configure_app, global_exception_handler

app = FastAPI()
configure_app(app)
app.add_exception_handler(Exception, global_exception_handler)


@app.post("/about-me")
async def about_me(user: models.User) -> Response:
    response = services.about_me(user)
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)

