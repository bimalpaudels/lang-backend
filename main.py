from fastapi import FastAPI
from llm import Llama
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from utils.helpers import build_user_context

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)


class User(BaseModel):
    full_name: str
    original: str
    current: str
    occupation: str
    target_language: str
    current_level: str
    target_level: str


ch = Llama()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/about-me")
async def about_me(user: User):
    user_context = build_user_context(user.model_dump())
    response = ch.about_me(user_context, prompt)
    return {"message": "success", "data": response}


prompt = """
    Generate me a 200 words Introduction paragraph, following the format:
    Target: <target_language_text>
    Translation: <English_translation>
    Ensure there are no extra sentences.
    """