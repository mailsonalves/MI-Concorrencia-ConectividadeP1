import random
import string
import uuid
from queue import Queue

class Voo():
    def __init__(self, origem: str, destino: str) -> None:
        self.id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.origem = origem
        self.destino = destino
        self.vagas = {'A1': False,'A2': False}
        self.disponibilidade = any(not ocupada for ocupada in self.vagas.values())
    
        
class Passagem():
    def __init__(self, id_voo:str, id_passageiro:str,  cpf:str ) -> None:
        #self.id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.id_voo = id_voo
        self.id_passageiro = id_passageiro
        self.cpf = cpf
        self.assento = ''
        
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
    
        
        
            
        