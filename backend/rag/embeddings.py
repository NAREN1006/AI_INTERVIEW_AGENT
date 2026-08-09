from sentence_transformers import SentenceTransformer


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    """
    Convert text chunks into numerical vectors.
    """

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True
    )

    return embeddings