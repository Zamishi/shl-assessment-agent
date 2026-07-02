from dataclasses import dataclass, field
from typing import List


@dataclass
class Assessment:
    entity_id: str
    name: str
    link: str
    description: str
    duration: str

    job_levels: List[str] = field(default_factory=list)
    languages: List[str] = field(default_factory=list)
    keys: List[str] = field(default_factory=list)

    remote: str = ""
    adaptive: str = ""

    def searchable_text(self) -> str:
        """
        Combines searchable fields into one lowercase string.
        Used by the retriever.
        """
        return " ".join([
            self.name,
            self.description,
            " ".join(self.keys),
            " ".join(self.job_levels),
            " ".join(self.languages),
            self.duration,
            self.remote,
            self.adaptive
        ]).lower()