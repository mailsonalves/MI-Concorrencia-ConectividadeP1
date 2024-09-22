import random
import string

class Voo():
    """
    Classe que representa um voo no sistema de compra de passagens aéreas.

    Atributos:
    ----------
    id : str
        Identificador único do voo, gerado aleatoriamente com 6 caracteres alfanuméricos.
    origem : str
        Cidade ou local de origem do voo.
    destino : str
        Cidade ou local de destino do voo.
    vagas : dict
        Dicionário que representa a ocupação dos assentos no voo. As chaves são os números dos assentos e os valores indicam se o assento está ocupado (True) ou não (False).
    disponibilidade : bool
        Indica se o voo ainda tem assentos disponíveis para reserva (True se houver pelo menos um assento livre, False caso contrário).

    Métodos:
    --------
    __init__(self, origem: str, destino: str) -> None
        Inicializa uma instância da classe Voo com os parâmetros fornecidos.
    """

    def __init__(self, origem: str, destino: str) -> None:
        """
        Inicializa um novo voo com origem, destino e um ID gerado aleatoriamente.

        Parâmetros:
        -----------
        origem : str
            Cidade ou local de origem do voo.
        destino : str
            Cidade ou local de destino do voo.
        """
        self.id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.origem = origem
        self.destino = destino
        self.preco = 0
        self.vagas = {'A1': False, 'A2': False}
        self.disponibilidade = any(not ocupada for ocupada in self.vagas.values())
