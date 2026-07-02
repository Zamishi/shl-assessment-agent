import re

from app.llm import (
    generate_reply,
    decide_action,
    generate_comparison
)
from app.retriever import Retriever


class SHLAgent:

    def __init__(self, retriever: Retriever):
        self.retriever = retriever

    def chat(self, messages):

        # -----------------------------
        # Collect all user messages
        # -----------------------------
        user_messages = [
            message["content"]
            for message in messages
            if message["role"] == "user"
        ]

        conversation = " ".join(user_messages)
        conversation_lower = conversation.lower()

        # -----------------------------
        # Rule 1 : Clarify vague queries
        # -----------------------------
        if len(conversation.split()) <= 3:
            return {
                "reply": "Could you tell me the role you're hiring for, the required skills, and the experience level?",
                "recommendations": [],
                "end_of_conversation": False
            }

        vague_phrases = [
            "need assessment",
            "recommend assessment",
            "assessment",
            "test",
            "recommend test"
        ]

        if conversation_lower.strip() in vague_phrases:
            return {
                "reply": "Could you tell me the role you're hiring for, the required skills, and the experience level?",
                "recommendations": [],
                "end_of_conversation": False
            }

        # -----------------------------
        # Rule 2 : Decide intent
        # -----------------------------
        if (
            "compare" in conversation_lower
            or "difference" in conversation_lower
            or " vs " in conversation_lower
        ):
            action = "COMPARE"
        else:
            action = decide_action(conversation)

        print("Detected Action:", action)

        # -----------------------------
        # Rule 3 : Compare assessments
        # -----------------------------
        if action == "COMPARE":

            parts = re.split(
                r"\band\b|\bvs\b",
                conversation,
                flags=re.IGNORECASE
            )

            if len(parts) >= 2:

                first = parts[0].replace("compare", "").strip()
                second = parts[1].strip()

                assessment1 = self.retriever.find_by_name(first)
                assessment2 = self.retriever.find_by_name(second)

                if assessment1 and assessment2:

                    reply = generate_comparison(
                        assessment1,
                        assessment2
                    )

                    return {
                        "reply": reply,
                        "recommendations": [
                            {
                                "name": assessment1.name,
                                "url": assessment1.link,
                                "test_type": assessment1.keys[0] if assessment1.keys else "General"
                            },
                            {
                                "name": assessment2.name,
                                "url": assessment2.link,
                                "test_type": assessment2.keys[0] if assessment2.keys else "General"
                            }
                        ],
                        "end_of_conversation": True
                    }

        # -----------------------------
        # Rule 4 : Refuse off-topic
        # -----------------------------
        if action == "REFUSE":
            return {
                "reply": "I'm designed to answer questions only about SHL assessments and assessment recommendations.",
                "recommendations": [],
                "end_of_conversation": True
            }

        # -----------------------------
        # Rule 5 : Retrieve assessments
        # -----------------------------
        results = self.retriever.search(conversation)

        recommendations = []

        for assessment in results:
            recommendations.append(
                {
                    "name": assessment.name,
                    "url": assessment.link,
                    "test_type": assessment.keys[0] if assessment.keys else "General"
                }
            )

        # -----------------------------
        # Rule 6 : No matches
        # -----------------------------
        if not recommendations:
            return {
                "reply": "I couldn't find any suitable SHL assessments matching your request.",
                "recommendations": [],
                "end_of_conversation": True
            }

        # -----------------------------
        # Rule 7 : Generate response
        # -----------------------------
        reply = generate_reply(
            conversation,
            recommendations
        )

        return {
            "reply": reply,
            "recommendations": recommendations,
            "end_of_conversation": True
        }