@dataclass
class Project:
    id: str
    name: str
    description: str
    content_store: ContentStore

    def __init__(self, name: str, description: str, base_path: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.content_store = ContentStore(base_path)

    def initialize_with_questionnaire(self, questionnaire_content: Dict) -> None:
        """
        Initializes project with questionnaire content.

        Args:
            questionnaire_content: The completed questionnaire
        """
        # Store questionnaire content as a single-item list
        self.content_store.update_content(
            ArtifactType.QUESTIONNAIRE,
            [questionnaire_content]
        )