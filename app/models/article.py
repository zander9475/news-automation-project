from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Article:
    """
    Data class representing a single article.
    """
    title: str
    content: str
    source: str
    url: str
    authors: List[str] = field(default_factory=list)
    lead: Optional[str] = None

    def to_dict(self):
        """Converts the article object to a dictionary."""
        return {
            "title": self.title,
            "lead": self.lead,
            "content": self.content,
            "source": self.source,
            "url": self.url,
            "authors": self.authors,
            "lead": self.lead
        }