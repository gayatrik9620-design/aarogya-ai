
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.fitness_tool import get_fitness_summary

load_dotenv()

SAFETY_SYSTEM_PROMPT = """
You are Aarogya AI, a helpful and safe personal healthcare assistant.

Rules:
1. Give general health and wellness information only.
2. Never provide a definite medical diagnosis.
3. Never prescribe medicines or dosages.
4. For serious or persistent symptoms, recommend consulting a doctor.
5. For chest pain, severe breathing difficulty, sudden numbness,
   uncontrolled bleeding, or immediate danger, advise urgent medical
   care and calling India emergency number 112.
6. End health guidance with:
Disclaimer: I am an AI assistant, not a doctor.
Please consult a medical professional for advice.

User Query: {user_query}

Response:
"""


def get_chatbot_response(user_query: str) -> str:

    query = user_query.lower().strip()

    fitness_keywords = [
        "fitness summary",
        "my health data",
        "my steps",
        "my sleep",
        "my weight",
        "health report",
        "fitness report",
        "health summary",
        "show my health",
        "show fitness",
        "health statistics",
    ]

    if any(keyword in query for keyword in fitness_keywords):
        return get_fitness_summary()

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        return "Error: GOOGLE_API_KEY missing in .env file."

    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-3.8-flash",
            google_api_key=api_key,
            temperature=0.3,
        )

        prompt = PromptTemplate(
            input_variables=["user_query"],
            template=SAFETY_SYSTEM_PROMPT,
        )

        chain = prompt | llm | StrOutputParser()

        return chain.invoke({"user_query": user_query})

    except Exception as e:
        return f"Unable to get chatbot response: {e}"
