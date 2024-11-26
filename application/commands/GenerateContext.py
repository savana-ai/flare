from dataclasses import dataclass
from typing import List, Dict
from domain.Artifact import Artifact, PromptTemplate

@dataclass
class GetContextCommand:
    """
    Command to retrieve context from artifacts referenced in a template.
    """
    artifact: Artifact
    template: PromptTemplate

    def execute(self) -> List[Dict]:
        """
        Execute the get context command.

        Returns:
            List[Dict]: Combined content from referenced artifacts
        """
        return self.artifact.get_context(self.template)

