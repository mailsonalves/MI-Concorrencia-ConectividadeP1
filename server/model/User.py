import uuid
from uuid import UUID

class User():
    def __init__(self, password: str, username: str) -> None:
        self.id_user : UUID = uuid.uuid4()
        self.username : str = username
        self.password : str = password
        self.cpf : str = ''
        self.name : str = ''
        self.passagens : list[str] = []