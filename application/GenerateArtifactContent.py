# application/services/artifact_app_service.py

from dataclasses import dataclass
from typing import Dict, Any

from application.queries.artifact_queries import GetPromptTemplateQuery, GetContextQuery
from application.commands.artifact_commands import (
    GetContextCommand, 
    GeneratePromptCommand, 
    UpdateContentCommand
)
from domain.Artifact import Artifact, ContentStore


@dataclass
class ArtifactContentService:
    """
    App service for generating and updating artifact content.
    """
    content_store: ContentStore

    def generate_artifact_content(self, input_data: Dict[str, Any]) -> None:
        """
        Orchestrate the process of generating artifact content.

        Args:
            input_data: Dictionary containing input parameters
        """
        # Get prompt template
        get_template_query = GetPromptTemplateQuery(
            criteria={"artifact_type": input_data['artifact_type']}
        )
        templates = get_template_query.execute()
        
        if not templates:
            raise ValueError(f"No template found for artifact type: {input_data['artifact_type']}")
        
        template = templates[0]

        # Create artifact
        artifact = Artifact(
            project_id=input_data['project_id'], 
            type=input_data['artifact_type'], 
            content_store=self.content_store
        )

        # Get context
        get_context_command = GetContextCommand(
            artifact=artifact, 
            template=template
        )
        contexts = get_context_command.execute()

        # Generate prompts
        generate_prompt_command = GeneratePromptCommand(
            artifact=artifact, 
            template=template
        )
        prompts = generate_prompt_command.execute()

        # Here you would typically integrate with an LLM or content generation service
        # For now, we'll simulate content generation
        generated_content = [
            {"id": prompt.id, "content": f"Generated content for {prompt.template}"} 
            for prompt in prompts
        ]

        # Update content
        update_content_command = UpdateContentCommand(
            artifact=artifact, 
            content=generated_content
        )
        update_content_command.execute()