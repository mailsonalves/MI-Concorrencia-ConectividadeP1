import random
import string

class Voo():
    def __init__(self, origem: str, destino: str) -> None:
        self.id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.origem = origem
        self.destino = destino
        self.vagas = {'A1': False,'A2': False}
        self.disponibilidade = any(not ocupada for ocupada in self.vagas.values())