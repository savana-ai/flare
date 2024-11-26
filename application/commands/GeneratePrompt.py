from dataclasses import dataclass
from typing import List, Dict
from domain.Artifact import Artifact, PromptTemplate

@dataclass
class GeneratePromptCommand:
    """
    Command to generate prompts based on a template and artifact contexts.
    """
    artifact: Artifact
    template: PromptTemplate

    def execute(self) -> List['Prompt']:
        """
        Execute the generate prompt command.

        Returns:
            List[Prompt]: List of generated prompts
        """
        return self.artifact.create_prompt(self.template)

