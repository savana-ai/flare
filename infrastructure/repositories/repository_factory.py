from typing import Literal, Union
from sql_repository import SQLRepository
from json_repository import JSONRepository
from base_repository import BaseRepository

class RepositoryFactory:
    """
    A factory class for creating repository instances based on the specified type.
    
    Provides a centralized method to instantiate different types of repositories
    with a consistent interface.
    """
    
    @staticmethod
    def create_repo(
        repo_type: Literal["SQL", "JSON"], 
        db_location: str
    ) -> Union[SQLRepository, JSONRepository]:
        """
        Create a repository instance based on the specified type.
        
        Args:
            repo_type (str): Type of repository to create. 
                              Must be either "SQL" or "JSON".
            db_location (str): Path to the database or directory
        
        Returns:
            A repository instance (SQLRepository or JSONRepository)
        
        Raises:
            ValueError: If an unknown repository type is provided
        """
        if repo_type == "SQL":
            return SQLRepository(db_path=db_location)
        elif repo_type == "JSON":
            return JSONRepository(db_directory=db_location)
        else:
            raise ValueError(f"Unknown repository type: {repo_type}")