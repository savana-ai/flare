from dataclasses import dataclass
from typing import List, Dict, Optional
from infrastructure.repositories import prompt_store


@dataclass
class GetPromptTemplateQuery:
    """
    Query to retrieve prompt templates from the repository.
    """
    identifier: Optional[str] = None
    criteria: Optional[Dict] = None

    def execute(self) -> List[Dict]:
        """
        Execute the query to retrieve prompt templates.

        Returns:
            List[Dict]: Retrieved prompt templates
        """
        if self.identifier:
            # If an identifier is provided, load a specific template
            template = prompt_store.load(self.identifier)
            return [template] if template else []
        
        if self.criteria:
            # If criteria are provided, find templates matching those criteria
            return prompt_store.find_by(self.criteria)
        
        # If no identifier or criteria, return all prompt templates
        return prompt_store.get_all()

