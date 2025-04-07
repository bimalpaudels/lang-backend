from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, StreamingResponse
from starlette import status
import edge_tts
from core import services, models
from config import configure_app, global_exception_handler
from core.models import BaseResponse

app = FastAPI()
configure_app(app)
app.add_exception_handler(Exception, global_exception_handler)


@app.post("/about-me")
async def about_me(user: models.User) -> Response:
    response = services.about_me(user)
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)


@app.post("/speak")
async def speak(text: str) -> StreamingResponse:

    return StreamingResponse(services.text_to_speech(text),
                             media_type="audio/mpeg",
                             headers={
                                 "X-Response-Metadata": BaseResponse(
                                     success=True,
                                     message="Streaming audio",
                                     data={"format": "audio/mpeg"}
                                 ).model_dump_json()
                             })


