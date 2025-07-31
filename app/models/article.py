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
    keyword: str = "Manual"
    authors: List[str] = field(default_factory=list)
    url: Optional[str] = None
    lead: Optional[str] = None

    def to_dict(self):
        """Converts the Article object to a dictionary."""
        return {
            "title": self.title,
            "lead": self.lead,
            "content": self.content,
            "source": self.source,
            "url": self.url,
            "authors": self.authors,
            "keyword": self.keyword
        }