import os

from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def decide_action(conversation: str):

    prompt = f"""
You are an AI agent for SHL Assessment recommendations.

Classify the user's latest intent.

Return ONLY ONE WORD.

CLARIFY
RECOMMEND
COMPARE
REFUSE

Conversation:
{conversation}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        action = response.text.upper()

        if "CLARIFY" in action:
            return "CLARIFY"

        if "COMPARE" in action:
            return "COMPARE"

        if "REFUSE" in action:
            return "REFUSE"

        return "RECOMMEND"

    except Exception as e:

        print("Intent Classification Error:", e)

        # Safe fallback
        return "RECOMMEND"


def generate_reply(user_query: str, recommendations: list):

    if not recommendations:
        return "I couldn't find any suitable SHL assessments."

    catalog = ""

    for item in recommendations:
        catalog += (
            f"- {item['name']}\n"
            f"  URL: {item['url']}\n"
            f"  Type: {item['test_type']}\n\n"
        )

    prompt = f"""
You are an SHL Assessment Recommendation Assistant.

Use ONLY the assessments provided below.

Do NOT invent new assessments.

If any recommended assessment is clearly unrelated to the user's requirement,
briefly mention that it may be less relevant.

User Requirement:
{user_query}

Recommended Assessments:

{catalog}

Write a concise recommendation.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text

    except Exception as e:

        print("Reply Generation Error:", e)

        return (
            "I found relevant SHL assessments for your request. "
            "Please review the recommendations below."
        )
def generate_comparison(assessment1, assessment2):

        prompt = f"""
        You are an SHL Assessment expert.

        Compare ONLY these two SHL assessments.

        Assessment 1
        Name: {assessment1.name}
        Description: {assessment1.description}
        Duration: {assessment1.duration}
        Categories: {", ".join(assessment1.keys)}

        Assessment 2
        Name: {assessment2.name}
        Description: {assessment2.description}
        Duration: {assessment2.duration}
        Categories: {", ".join(assessment2.keys)}

        Instructions:
        - Compare their purpose.
        - Mention what each assessment measures.
        - Mention when each should be used.
        - Mention the major differences.
        - Use ONLY the information provided.
        - Do not invent anything.
        """

        try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )

                return response.text

        except Exception as e:

                print("Comparison Error:", e)

                return (
                    f"{assessment1.name} and {assessment2.name} are two SHL "
                    "assessments. Please refer to their catalog pages for details."
                )