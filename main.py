from fastapi import FastAPI
from llm import ContextHandler, build_user_context

app = FastAPI()
ch = ContextHandler()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/about-me")
async def about_me():
    user_data = {
        "full_name": "Bimal Paudel",
        "from": "Kathmandu, Nepal",
        "current": "Berlin, Germany",
        "occupation": "Student",
        "target_language": "German",
        "current_level": "None",
        "target_level": "A1",
    }
    user_context = build_user_context(user_data)
    response = ch.about_me(user_context)
    return {"message": "success", "data": response}
