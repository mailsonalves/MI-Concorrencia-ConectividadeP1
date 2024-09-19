

class Passagem():
    """
    Classe que representa uma passagem de voo no sistema.

    Atributos:
    ----------
    id_voo : str
        Identificador do voo ao qual a passagem está associada.
    id_passageiro : str
        Identificador do passageiro que comprou a passagem.
    cpf : str
        CPF do passageiro que comprou a passagem.
    assento : str
        Número do assento reservado pelo passageiro (inicialmente vazio).

    Métodos:
    --------
    __init__(self, id_voo: str, id_passageiro: str, cpf: str) -> None
        Inicializa uma instância da classe Passagem com os parâmetros fornecidos.
    """

    def __init__(self, id_voo: str, id_passageiro: str, cpf: str) -> None:
        """
        Inicializa uma nova passagem para um voo específico.

        Parâmetros:
        -----------
        id_voo : str
            O identificador do voo.
        id_passageiro : str
            O identificador do passageiro.
        cpf : str
            O CPF do passageiro.
        """
        # self.id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.id_voo = id_voo
        self.id_passageiro = id_passageiro
        self.cpf = cpf
        self.assento = ''
