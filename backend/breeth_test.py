import requests

BREETH_API_KEY = "ck_live_jYV7dJwg-JtDEo-4YQFAzQlWjy3UTVQ-fJ-FrhpY8kY"

URL = "https://api.thebreeth.com/v1/search"

headers = {
    "Authorization": f"Bearer {BREETH_API_KEY}",
    "Content-Type": "application/json",
}

data = {
    "query": "What does the candidate know about Python, Machine Learning and NLP?",
    "limit": 5,
}

response = requests.post(
    URL,
    headers=headers,
    json=data,
)

print("Status:", response.status_code)
print("Response:")
print(response.text)