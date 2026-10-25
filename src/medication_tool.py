import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.fitness_tool import get_fitness_summary
from src.medication_tool import check_medication_interaction

load_dotenv()


SAFETY_SYSTEM_PROMPT = """You are Aarogya AI, a helpful, empathetic, and safe personal healthcare assistant.

CRITICAL SAFETY RULES:

1. Provide ONLY general informational and wellness guidance.
2. NEVER provide a definitive medical diagnosis.
3. NEVER prescribe, suggest, or recommend specific medicines, treatments, or dosages.
4. For serious or persistent symptoms, advise the user to consult a qualified healthcare professional.
5. EMERGENCY RULE:
If the user mentions chest pain, severe shortness of breath, sudden numbness,
uncontrolled bleeding, thoughts of self-harm, or suicide, immediately start your
response with a prominent emergency warning and advise urgent medical care
or calling India emergency services 112 or 108.
6. Always end your response with:

Disclaimer: I am an AI assistant, not a doctor. Please consult a medical professional for advice.

User Query: {user_query}

Response:
"""


def get_chatbot_response(user_query: str) -> str:

    # Fitness Summary Tool
    fitness_keywords = [
        "fitness summary",
        "health summary",
        "my fitness",
        "my health data",
        "steps",
        "sleep",
        "weight"
    ]

    if any(keyword in user_query.lower() for keyword in fitness_keywords):
        try:
            return get_fitness_summary()
        except Exception as e:
            return f"Unable to generate fitness summary: {str(e)}"

    # Medication Interaction Tool
    medication_keywords = [
        "medication interaction",
        "medicine interaction",
        "drug interaction",
        "check medicines",
        "check medication"
    ]

    if any(keyword in user_query.lower() for keyword in medication_keywords):

        # Example:
        # "Check medication interaction: aspirin, ibuprofen"
        text = user_query.split(":", 1)

        if len(text) == 2:
            medications = text[1].split(",")
            return check_medication_interaction(medications)

        return (
            "Please enter the medication names separated by commas.\n\n"
            "Example: Check medication interaction: aspirin, ibuprofen"
        )

    # Gemini AI response
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        return "⚠️ Error: GOOGLE_API_KEY missing in .env"

    try:

        llm = ChatGoogleGenerativeAI(
            model="gemini-3.8-flash",
            google_api_key=api_key,
            temperature=0.3
        )

        prompt = PromptTemplate(
            input_variables=["user_query"],
            template=SAFETY_SYSTEM_PROMPT
        )

        chain = prompt | llm | StrOutputParser()

        return chain.invoke({
            "user_query": user_query
        })

    except Exception as e:
        return f"⚠️ Error: {str(e)}"