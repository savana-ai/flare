import os
import json
from typing import Dict, Any, Optional, Union
from base_repository import BaseRepository
from repository_factory import RepositoryFactory

class ContentStore:
    """
    Manages artifact content storage using the repository pattern.
    
    Provides a flexible interface for storing and retrieving content.
    """
    
    def __init__(
        self, 
        repo_type: str = "JSON", 
        location: Optional[str] = None
    ):
        """
        Initialize the ContentStore with a specific repository type.
        
        Args:
            repo_type (str, optional): Type of repository to use. Defaults to "JSON".
            location (str, optional): Path for the repository. 
                                      Defaults to a path in the project's db directory.
        """
        # Determine the default location if not provided
        if location is None:
            base_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 
                '..', 
                'db'
            )
            os.makedirs(base_dir, exist_ok=True)
            location = os.path.join(base_dir, "content_store.json")
        
        # Create the repository
        self.repo = RepositoryFactory.create_repo(repo_type, location)
    
    def save(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Save content to the store.
        
        Args:
            content (str): The content to be saved
            metadata (dict, optional): Additional metadata for the content
        
        Returns:
            str: The identifier under which the content was saved
        """
        # Prepare the data to save
        data = metadata or {}
        data['content'] = content
        
        # Generate an ID if not provided
        if 'id' not in data:
            data['id'] = f"content_{len(self.repo.get_all()) + 1}"
        
        # Save the content
        return self.repo.save(data)
    
    def load(self, identifier: str) -> Optional[str]:
        """
        Load content from the store by its identifier.
        
        Args:
            identifier (str): The unique identifier of the content
        
        Returns:
            str or None: The loaded content, or None if not found
        """
        item = self.repo.load(identifier)
        return item.get('content') if item else None
    
    def delete(self, identifier: str) -> bool:
        """
        Delete content from the store.
        
        Args:
            identifier (str): The unique identifier of the content to delete
        
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        return self.repo.delete(identifier)
    
    def get_all(self) -> Dict[str, str]:
        """
        Retrieve all contents from the store.
        
        Returns:
            dict: A dictionary of artifact identifiers and their contents
        """
        return {
            item['id']: item['content'] 
            for item in self.repo.get_all() 
            if 'content' in item
        }
    
    def find_by(self, criteria: Dict[str, Any]) -> Dict[str, str]:
        """
        Find contents matching specific criteria.
        
        Args:
            criteria (dict): A dictionary of key-value pairs to match
        
        Returns:
            dict: Contents matching the criteria
        """
        matching_items = self.repo.find_by(criteria)
        return {
            item['id']: item['content'] 
            for item in matching_items 
            if 'content' in item
        }