from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime
import uuid
import json
import os
from pathlib import Path


@dataclass
class Artifact:
    id: str
    project_id: str
    type: ArtifactType
    content_store: ContentStore

    def __init__(self, project_id: str, type: ArtifactType, content_store: ContentStore):
        self.id = str(uuid.uuid4())
        self.project_id = project_id
        self.type = type
        self.content_store = content_store

    def get_context(self, template: PromptTemplate) -> List[Dict]:
        """
        Retrieves context from all artifacts referenced in the template's objects field.

        Args:
            template: PromptTemplate containing object references

        Returns:
            List[Dict]: Combined content from all referenced artifacts
        """
        contexts = []
        for obj_type in template.objects:
            # Get content list from referenced artifact's storage
            artifact_content = self.content_store.get_content(ArtifactType(obj_type))
            contexts.extend(artifact_content)  # Add all items from content list
        return contexts

    def create_prompt(self, template: PromptTemplate) -> List[Prompt]:
        """
        Creates prompts by combining template with context from referenced artifacts.

        Args:
            template: The prompt template to use

        Returns:
            List[Prompt]: List of prompts, one for each context item
        """
        # Get all context items
        contexts = self.get_context(template)

        # Create new prompt for each context item
        prompts = []
        template_dict = template.__dict__.copy()
        del template_dict['objects']  # Remove objects field

        for context_item in contexts:
            prompt = Prompt(
                template=template_dict,
                context=context_item
            )
            prompts.append(prompt)

        return prompts

    def update_content(self, content: List[Dict]) -> None:
        """
        Updates artifact content in storage.

        Args:
            content: New content list to store
        """
        self.content_store.update_content(self.type, content)
