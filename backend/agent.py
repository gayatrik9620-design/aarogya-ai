import os
from dotenv import load_dotenv

load_dotenv()


def get_health_agent_reply(question: str) -> str:

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        return (
            "Welcome to Aarogya AI! "
            "I received your question. "
            "Please configure your Gemini API key "
            "to enable AI responses."
        )

    try:
        from google import genai

        client = genai.Client(api_key=api_key)

        prompt = f"""
        You are Aarogya AI, a health information assistant.

        Your responsibilities:
        1. Provide general health information.
        2. Suggest healthy lifestyle habits.
        3. Give simple and understandable answers.
        4. Never diagnose diseases.
        5. Never prescribe medicines.
        6. Encourage users to consult healthcare professionals.

        User Question: {question}
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception:
        return (
            "Sorry, the AI service is temporarily unavailable. "
            "Please try again later."
        )