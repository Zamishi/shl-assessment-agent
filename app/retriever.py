from typing import List
from app.models import Assessment
from app.utils import preprocess_query


class Retriever:

    def __init__(self, assessments: List[Assessment]):

        # Build a searchable index once
        self.index = []

        for assessment in assessments:
            self.index.append({
                "assessment": assessment,
                "text": assessment.searchable_text()
            })
    
    def search(self, query: str, top_k: int = 10):

        tokens = preprocess_query(query)

        scored = []

        for item in self.index:

            assessment = item["assessment"]
            searchable_text = item["text"]

            score = 0
            matched_tokens = 0

            name = assessment.name.lower()
            keys = " ".join(assessment.keys).lower()

            for token in tokens:

                # Highest priority: assessment name
                if token == name:
                    score += 60
                    matched_tokens += 1

                elif token in name:
                    score += 30
                    matched_tokens += 1

                # Searchable text
                if token in searchable_text:
                    score += 10
                    matched_tokens += 1

                # Assessment category
                if token in keys:
                    score += 12
                    matched_tokens += 1

            # -----------------------------
            # Technology boosts
            # -----------------------------
            if "java" in tokens:

                if "java" in searchable_text:
                    score += 25
                else:
                    score -= 40

            if "python" in tokens:

                if "python" in searchable_text:
                    score += 25
                else:
                    score -= 40

            if "sql" in tokens:

                if "sql" in searchable_text:
                    score += 25
                else:
                    score -= 40

            if "javascript" in tokens:

                if "javascript" in searchable_text:
                    score += 25
                else:
                    score -= 40

            # Bonus for multiple keyword matches
            score += matched_tokens * 5

            # Ignore weak matches
            if score >= 30:
                scored.append((score, assessment))

        scored.sort(key=lambda x: x[0], reverse=True)

        return [assessment for score, assessment in scored[:top_k]]

    # def search(self, query: str, top_k: int = 10):

    #     tokens = preprocess_query(query)

    #     scored = []

    #     for item in self.index:

    #         assessment = item["assessment"]
    #         searchable_text = item["text"]

    #         score = 0
    #         matched_tokens = 0

    #         name = assessment.name.lower()
    #         keys = " ".join(assessment.keys).lower()

    #         for token in tokens:

    #             # Exact assessment name
    #             if token == name:
    #                 score += 60
    #                 matched_tokens += 1

    #             # Assessment title
    #             elif token in name:
    #                 score += 30
    #                 matched_tokens += 1

    #             # Anywhere in searchable text
    #             if token in searchable_text:
    #                 score += 10
    #                 matched_tokens += 1

    #             # Assessment category
    #             if token in keys:
    #                 score += 12
    #                 matched_tokens += 1

    #         # Bonus for multiple keyword matches
    #         score += matched_tokens * 5

    #         # Technology bonuses
    #         if "java" in tokens and "java" in searchable_text:
    #             score += 25

    #         if "python" in tokens and "python" in searchable_text:
    #             score += 25

    #         if "sql" in tokens and "sql" in searchable_text:
    #             score += 25

    #         # Ignore weak matches
    #         if score >= 25:
    #             scored.append((score, assessment))

    #     scored.sort(key=lambda x: x[0], reverse=True)

    #     return [assessment for score, assessment in scored[:top_k]]

    # --------------------------------------------------
    # Find a single assessment by its name
    # Used for comparison requests
    # --------------------------------------------------
    def find_by_name(self, name: str):

        name = name.lower().strip()

        best_match = None
        best_score = 0

        for item in self.index:

            assessment = item["assessment"]
            assessment_name = assessment.name.lower()

            score = 0

            # Exact match
            if assessment_name == name:
                return assessment

            # Partial match
            if name in assessment_name:
                score += 20

            # Word overlap
            for word in name.split():
                if word in assessment_name:
                    score += 5

            if score > best_score:
                best_score = score
                best_match = assessment

        return best_match