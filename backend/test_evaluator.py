from data_loader import load_curriculum
from answer_evaluator import evaluate_answer


curriculum = load_curriculum()

# Day 3
topic = curriculum["days"][2]

answer = """
I built a command-line chatbot using Ollama and a local AI model.
I created a FastAPI backend with a health endpoint.
For the frontend, I created a React application using Vite.
I connected the React frontend to the FastAPI backend.
I initialized the project with Git, committed the changes,
and published the project to GitHub.
"""

result = evaluate_answer(answer, topic)

print("\n===== EVALUATION RESULT =====\n")

print("Topic:")
print(topic["title"])

print("\nScore:")
print(result["score"])

print("\nStrengths:")
print(result["strengths"])

print("\nGaps:")
print(result["gaps"])

print("\nMatched Objectives:")
print(result["matched_objectives"])

print("\nMissed Objectives:")
print(result["missed_objectives"])

print("\nMatched Tools:")
print(result["matched_tools"])