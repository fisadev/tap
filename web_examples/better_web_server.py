#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["fastapi", "uvicorn"]
# ///
from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get("/get_likes/{word}")
async def get_likes(word: str):
    return {"received_word": word, "likes": 42}


uvicorn.run(app, host="0.0.0.0", port=5000)

