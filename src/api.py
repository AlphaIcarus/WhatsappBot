class BooklineAPI:

    def __init__(self) -> None:
        pass

    def insert_customer_email(self, email: str) -> None:
        """Insert an email in the database.
        
        If not successful, raise an InsertEmailError.
        """
        raise NotImplementedError


class InsertEmailError(Exception):
    pass
