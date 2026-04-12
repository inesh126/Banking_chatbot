import json
import hashlib
import math
import re
from functools import lru_cache

from config import KNOWLEDGE_BASE_FILE
from chromadb import Client
from chromadb.config import Settings


EMBEDDING_DIMENSION = 64


def _tokenize(text: str):
    return re.findall(r"[a-z0-9]+", text.lower())


def _embed_text(text: str):
    vector = [0.0] * EMBEDDING_DIMENSION
    tokens = _tokenize(text)
    if not tokens:
        return vector

    for token in tokens:
        bucket = int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16) % EMBEDDING_DIMENSION
        vector[bucket] += 1.0

    norm = math.sqrt(sum(value * value for value in vector))
    if not norm:
        return vector

    return [value / norm for value in vector]


def load_knowledge_documents():
    with KNOWLEDGE_BASE_FILE.open(encoding="utf-8") as file_obj:
        return json.load(file_obj)


@lru_cache(maxsize=1)
def get_knowledge_collection():
    documents = load_knowledge_documents()
    client = Client(Settings(anonymized_telemetry=False))
    collection = client.get_or_create_collection("banking_knowledge_base")
    collection.upsert(
        ids=[item["id"] for item in documents],
        documents=[item["text"] for item in documents],
        metadatas=[{"topic": item["topic"]} for item in documents],
        embeddings=[_embed_text(item["text"]) for item in documents],
    )
    return collection


def search_knowledge_base(query: str, top_k: int = 3):
    collection = get_knowledge_collection()
    results = collection.query(
        query_embeddings=[_embed_text(query)],
        n_results=top_k,
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]
    ids = results.get("ids", [[]])[0]

    matches = []
    for item_id, document, metadata, distance in zip(ids, documents, metadatas, distances):
        matches.append(
            {
                "id": item_id,
                "topic": (metadata or {}).get("topic"),
                "text": document,
                "score": round(1 / (1 + float(distance)), 4) if distance is not None else None,
            }
        )

    return matches
