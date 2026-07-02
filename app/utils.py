from app.models import Assessment
import json
import re
from pathlib import Path

STOP_WORDS = {
    "a", "an", "the", "for", "of", "with", "and",
    "to", "need", "needs", "looking", "hire",
    "hiring", "years", "year", "experience",
    "experienced", "level", "role", "position",
    "candidate", "someone", "person"
}

# Expand common hiring terms into search-friendly keywords
SYNONYMS = {
    "developer": ["developer", "programming"],
    "engineer": ["developer", "engineering"],
    "backend": ["backend", "enterprise"],
    "frontend": ["frontend", "javascript"],
    "fullstack": ["java", "javascript"],
    "software": ["developer"],
    "manager": ["manager"],
    "graduate": ["graduate"],
    "entry": ["entry-level"],
    "senior": ["professional"],
    "mid": ["mid-professional"],
    "lead": ["manager"],
    "java": ["java"],
    "python": ["python"],
    "sql": ["sql"],
    "javascript": ["javascript"],
    "personality": ["personality"],
    "aptitude": ["ability", "aptitude"],
    "reasoning": ["reasoning"],
    "cognitive": ["ability"],
    "communication": ["competencies"],
    "leadership": ["competencies"],
    "sales": ["sales"],
    "customer": ["customer"],
    "finance": ["finance"],
    "ai": ["ai"],
}


def preprocess_query(query: str):

    # lowercase
    query = query.lower()

    # remove punctuation
    query = re.sub(r"[^\w\s-]", " ", query)

    words = query.split()

    expanded = []

    for word in words:

        if word in STOP_WORDS:
            continue

        expanded.append(word)

        if word in SYNONYMS:
            expanded.extend(SYNONYMS[word])

    # remove duplicates while preserving order
    cleaned = []

    seen = set()

    for token in expanded:
        if token not in seen:
            seen.add(token)
            cleaned.append(token)

    return cleaned


def load_catalog():
    """
    Loads the SHL product catalog JSON.
    """

    data_path = Path("data") / "shl_catalog.json"

    with open(data_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    assessments = []

    for item in catalog:

        assessments.append(
            Assessment(
                entity_id=item.get("entity_id", ""),
                name=item.get("name", ""),
                link=item.get("link", ""),
                description=item.get("description", ""),
                duration=item.get("duration", ""),
                job_levels=item.get("job_levels", []),
                languages=item.get("languages", []),
                remote=item.get("remote", ""),
                adaptive=item.get("adaptive", ""),
                keys=item.get("keys", []),
            )
        )

    return assessments