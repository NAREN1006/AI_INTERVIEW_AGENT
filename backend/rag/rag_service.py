
from rag.embeddings import create_embeddings
from rag.vector_store import get_collection
from rag.retriever import retrieve_documents


def retrieve_context(query, top_k=2):
    """
    Retrieve the most relevant knowledge
    from the ChromaDB vector store.
    """

    # -------------------------------------------------
    # Validate query
    # -------------------------------------------------

    if not query or not str(query).strip():
        return []

    query = str(query).strip()

    try:

        # -------------------------------------------------
        # Create embedding for user's query
        # -------------------------------------------------

        embedding = create_embeddings(
            [query]
        )[0]

        # -------------------------------------------------
        # Get ChromaDB collection
        # -------------------------------------------------

        collection = get_collection()

        # -------------------------------------------------
        # Retrieve relevant documents
        # -------------------------------------------------

        results = retrieve_documents(
            collection,
            embedding,
            top_k=top_k
        )

        if not results:
            return []

        # -------------------------------------------------
        # Extract documents
        # -------------------------------------------------

        documents = results.get(
            "documents",
            []
        )

        # -------------------------------------------------
        # ChromaDB may return nested list
        # Example:
        # [["document 1", "document 2"]]
        # -------------------------------------------------

        if (
            documents
            and isinstance(
                documents[0],
                list
            )
        ):
            documents = documents[0]

        # -------------------------------------------------
        # Remove empty documents
        # -------------------------------------------------

        documents = [
            str(document)
            for document in documents
            if document
        ]

        return documents

    except Exception as error:

        print(
            f"RAG retrieval error: {error}"
        )

        # -------------------------------------------------
        # Do not stop the interview if RAG fails
        # -------------------------------------------------

        return []
