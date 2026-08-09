import requests
import os


BREETH_API_KEY = os.getenv("BREETH_API_KEY")

BREETH_BASE_URL = "https://api.thebreeth.com/v1"


def save_memory(content, group_id="default"):
    """
    Store candidate/interview information in Breeth.
    """

    if not BREETH_API_KEY:
        print("WARNING: BREETH_API_KEY is not configured.")
        return None

    try:
        response = requests.post(
            f"{BREETH_BASE_URL}/episodes",
            headers={
                "Authorization": f"Bearer {BREETH_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "content": content,
                "group_id": group_id,
                "extract_intent": True,
            },
            timeout=20,
        )

        if response.status_code != 200:
            print(
                "Breeth save failed:",
                response.status_code,
                response.text,
            )
            return None

        data = response.json()

        print(
            "Breeth memory saved:",
            data.get("episode_name"),
        )

        return data

    except Exception as error:
        print(
            "Breeth save error:",
            error,
        )

        return None


def search_memory(query, limit=5):
    """
    Search previously stored candidate/interview memory.
    """

    if not BREETH_API_KEY:
        print("WARNING: BREETH_API_KEY is not configured.")
        return []

    try:
        response = requests.post(
            f"{BREETH_BASE_URL}/search",
            headers={
                "Authorization": f"Bearer {BREETH_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "query": query,
                "limit": limit,
            },
            timeout=20,
        )

        if response.status_code != 200:
            print(
                "Breeth search failed:",
                response.status_code,
                response.text,
            )
            return []

        data = response.json()

        return data

    except Exception as error:
        print(
            "Breeth search error:",
            error,
        )

        return []