from fastapi import FastAPI, Response, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from starlette import status
from core import services, models
from config import configure_app, global_exception_handler
from core.ai import GPT
from core.models import BaseResponse
from dependencies import get_gpt


app = FastAPI()
configure_app(app)
app.add_exception_handler(Exception, global_exception_handler)


@app.post("/about-me")
async def about_me(user: models.User, gpt: GPT = Depends(get_gpt)) -> Response:
    response = services.translate_user_introduction(user, gpt)
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


@app.post("/detailed-meaning")
async def detailed_meaning(context: models.DetailedMeaning, gpt: GPT = Depends(get_gpt)) -> Response:
    response = services.detailed_description(context, gpt)
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)

