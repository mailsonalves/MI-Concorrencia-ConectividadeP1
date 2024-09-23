import random 
import string

class Passagem():
    def __init__(self, id_voo:str, id_passageiro:str,  cpf:str ) -> None:
        self.id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.id_voo = id_voo
        self.id_passageiro = id_passageiro
        self.cpf = cpf
        self.assento = ''