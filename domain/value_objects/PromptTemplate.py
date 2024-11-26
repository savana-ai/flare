@dataclass
class PromptTemplate:
    subject: str
    description: str
    instructions: str
    objects: List[str]  # References to other artifact types needed as context
    template: Dict
