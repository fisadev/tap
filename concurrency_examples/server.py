#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["fastapi", "uvicorn"]
# ///
"""Very simple server, with an endpoint that receives a word and returns a number of likes for it."""

from asyncio import sleep
from random import randint, random
from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get("/get_likes/{word}")
async def get_likes(word: str):
    await sleep(random())  # simulate some processing time
    return {"word": word, "likes": randint(0, 100)}


uvicorn.run(app, host="0.0.0.0", port=5000)
