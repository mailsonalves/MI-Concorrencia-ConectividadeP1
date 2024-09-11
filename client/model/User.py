import uuid
from uuid import UUID
from model.Passagem import Passagem
from model.Voo import Voo

class User():
    def __init__(self, password: str, username: str) -> None:
        self.id_user = uuid.uuid4()
        self.username = username
        self.password = password
        self.cpf = ''
        self.name = ''
        self.passagens = []
    
    def comprar_passagem(self, voo: Voo, assento:str, cpf: str):
        if voo.disponibilidade == True:
            if voo.vagas[assento] == False:
                passagem = Passagem(voo.id, self.id_user, cpf)
                passagem.assento = assento
                return passagem
            else:
                return 'Ocupado'
        else:
            return False