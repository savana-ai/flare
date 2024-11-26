from dataclasses import dataclass
from typing import List, Dict, Optional
from infrastructure.repositories import content_store


@dataclass
class GetContextQuery:
    """
    Query to retrieve context from content store.
    """
    artifact_type: str
    criteria: Optional[Dict] = None

    def execute(self) -> List[Dict]:
        """
        Execute the query to retrieve context for a specific artifact type.

        Returns:
            List[Dict]: Retrieved context items
        """
        # If no specific criteria, retrieve all content for the artifact type
        if not self.criteria:
            return content_store.find_by({"type": self.artifact_type})
        
        # If criteria are provided, find context items matching those criteria
        criteria_with_type = self.criteria.copy()
        criteria_with_type["type"] = self.artifact_type
        
        return content_store.find_by(criteria_with_type)