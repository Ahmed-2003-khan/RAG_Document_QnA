from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_utils import get_vector_store, get_answer
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# In-memory vector store cache
vector_store = None

class Query(BaseModel):
    question: str

@app.post("/embed")
def embed_docs():
    global vector_store
    vector_store = get_vector_store()
    return {"status": "Vector DB ready"}

@app.post("/ask")
def ask_question(query: Query):
    if not vector_store:
        return {"error": "Vector DB not initialized"}
    answer, context_docs = get_answer(query.question, vector_store)
    return {
        "answer": answer,
        "context": [doc.page_content for doc in context_docs]
    }
