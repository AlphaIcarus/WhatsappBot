class Classifier:

    def __init__(self, language: str) -> None:
        self.language = language

    def extract_intent(self, query: str) -> str:
        """Given a query, return the detected intent."""
        raise NotImplementedError
