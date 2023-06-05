import os
import logging
import sqlite3
from typing import List

import numpy as np
import openai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

from server.scraper import STORAGE_PATH, Sitting
from server.vectors import LocalStore

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(message)s")
LOGGER = logging.getLogger("server")

model = SentenceTransformer("all-MiniLM-L6-v2")
store = LocalStore()
openai.api_key = os.getenv("OPENAI_API_KEY")


class Question(BaseModel):
    question: str


class Answer(BaseModel):
    answer: str
    sources: List[Sitting]


origins = ["*"]

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    con = sqlite3.connect(os.path.join(STORAGE_PATH, "database.db"))
    try:
        cur = con.cursor()
        store.reset(cur)
        cur.close()
    except sqlite3.Error as error:
        LOGGER.error("Failed to read data from table", error)
    finally:
        if con:
            con.close()
            print("The Sqlite connection is closed")


@app.post("/answers")
async def create_item(question: Question):
    con = sqlite3.connect(os.path.join(STORAGE_PATH, "database.db"))
    try:
        cur = con.cursor()
        answer = get_answer(cur, question.question)
        return answer
    except sqlite3.Error as error:
        LOGGER.error("Failed to read data from table", error)
    finally:
        if con:
            con.close()
            print("The Sqlite connection is closed")


def get_answer(cur, query: str) -> Answer:
    embedding = model.encode(query, convert_to_numpy=True, normalize_embeddings=True)
    sources = store.get_sources(cur, embedding)
    prompt = create_prompt(query, sources)
    answer = ""
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
        )
        answer = completion.choices[0].message.content
    except:
        LOGGER.error("Something went wrong getting openai answer - returning null")
    return Answer(answer=answer, sources=sources)


def create_prompt(query: str, sources: List[Sitting]) -> str:
    prompt = "Please answer the following question based on the context provided and any other knowledge you may have:\n"
    prompt += f"Question: {query}\n"
    prompt += "Sources:\n\n"
    for source in sources:
        prompt += (
            f"Title: {source.title}, Date: {source.date}, Content: {source.text}\n\n"
        )

    return prompt
