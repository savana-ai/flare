# application/services/artifact_app_service.py
from dataclasses import dataclass
from typing import Dict, Any, List

from application.queries import GetPromptTemplateQuery, GetContextQuery
from application.commands import (
    GetContextCommand, 
    GeneratePromptCommand, 
    UpdateContentCommand
)

from domain.Artifact import Artifact
from domain.value_objects.artifact_type import ArtifactType
from infrastructure.repositories.stores import create_content_store

@dataclass
class ArtifactContentService:
    """
    App service for generating and updating artifact content for a specific project.
    """
    project_name: str
    
    def generate_artifact_content(self, artifact_type: ArtifactType) -> None:
        """
        Orchestrate the process of generating artifact content for a specific project.

        Args:
            artifact_type: Type of artifact to generate
        
        Returns:
            None
        """
        # Create project-specific content store
        content_store = create_content_store(self.project_name)
        
        # Get prompt template
        get_template_query = GetPromptTemplateQuery(
            criteria={"artifact_type": artifact_type}
        )
        templates = get_template_query.execute()
        
        if not templates:
            raise ValueError(f"No template found for artifact type: {artifact_type}")
        
        template = templates[0]

        # Create artifact
        artifact = Artifact(
            project_id=project_id,  # You'll need to pass this or derive from project_name 
            type=artifact_type, 
            content_store=content_store
        )

        # Get context
        get_context_query = GetContextQuery(artifact_type=artifact_type)
        contexts = get_context_query.execute()

        # Generate prompts
        prompts = artifact.create_prompt(template)

        # Here you would typically integrate with an LLM or content generation service
        # For now, we'll simulate content generation
        generated_content = [
            {"id": prompt.id, "content": f"Generated content for {prompt.template}"} 
            for prompt in prompts
        ]

        # Update content
        artifact.update_content(generated_content)