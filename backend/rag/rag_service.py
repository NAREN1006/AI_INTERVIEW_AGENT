def retrieve_context(query, top_k=2):
    """
    Lightweight deployment version.

    RAG is disabled for the 512 MB deployment environment.
    The interview system continues to work without retrieved context.
    """

    if not query or not str(query).strip():
        return []

    return []