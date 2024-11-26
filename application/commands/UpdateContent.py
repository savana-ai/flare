from dataclasses import dataclass
from typing import List, Dict
from domain.Artifact import Artifact, PromptTemplate

@dataclass
class UpdateContentCommand:
    """
    Command to update artifact content in storage.
    """
    artifact: Artifact
    content: List[Dict]

    def execute(self) -> None:
        """
        Execute the update content command.
        """
        self.artifact.update_content(self.content)