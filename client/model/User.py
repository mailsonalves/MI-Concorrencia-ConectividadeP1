import uuid
from uuid import UUID
from model.Passagem import Passagem
from model.Voo import Voo

class User():
    """
    Classe que representa um usuário no sistema de compra de passagens aéreas.
    
    Atributos:
    ----------
    id_user : UUID
        Identificador único do usuário gerado automaticamente.
    username : str
        Nome de usuário para login.
    password : str
        Senha do usuário.
    cpf : str
        CPF do usuário (inicialmente vazio).
    name : str
        Nome do usuário (inicialmente vazio).
    passagens : list
        Lista de passagens compradas pelo usuário (inicialmente vazia).

    Métodos:
    --------
    __init__(self, password: str, username: str) -> None
        Inicializa a instância da classe User com os atributos fornecidos.

    comprar_passagem(self, voo: Voo, assento: str, cpf: str)
        Permite que o usuário compre uma passagem para um voo específico.
        Retorna a instância da passagem se a compra for bem-sucedida.
        Retorna 'Ocupado' se o assento estiver ocupado.
        Retorna False se o voo não estiver disponível.
    """

    def __init__(self, password: str, username: str) -> None:
        """
        Inicializa um novo usuário.

        Parâmetros:
        -----------
        password : str
            A senha do usuário.
        username : str
            O nome de usuário.
        """
        self.id_user = uuid.uuid4()
        self.username = username
        self.password = password
        self.cpf = ''
        self.name = ''
        self.passagens = []
    
    def comprar_passagem(self, voo: Voo, assento: str, cpf: str):
        """
        Permite ao usuário comprar uma passagem para um voo específico.

        Parâmetros:
        -----------
        voo : Voo
            O objeto Voo para o qual o usuário deseja comprar a passagem.
        assento : str
            O assento que o usuário deseja reservar no voo.
        cpf : str
            O CPF do usuário para associar à passagem.

        Retorna:
        --------
        Passagem
            Retorna uma instância da classe Passagem se a compra for bem-sucedida.
        str
            Retorna 'Ocupado' se o assento já estiver reservado.
        bool
            Retorna False se o voo não estiver disponível.
        """
        if voo.disponibilidade:
            if not voo.vagas[assento]:
                passagem = Passagem(voo.id, self.id_user, cpf)
                passagem.assento = assento
                return passagem
            else:
                return 'Ocupado'
        else:
            return False
    
    def listar_passsagens(self, passagens_de_voos, voos):
        list_voos = []
        for passagem in passagens_de_voos:
            for voo in voos:
                if voo.id == passagem.id_voo:
                    list_voos.append(voo)
        return list_voos