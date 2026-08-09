import numpy as np


def retrieve_documents(
    collection,
    query_embedding,
    top_k=3
):
    """
    Search ChromaDB for the most relevant chunks.
    """

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=top_k
    )

    return results