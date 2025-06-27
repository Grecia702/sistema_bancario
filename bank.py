from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })


class Conta:
    def __init__(self, numero, agencia, cliente):
        self._saldo = 0
        self.numero = numero
        self.agencia = agencia
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, "0001", cliente)

    def sacar(self, valor):
        saldo = self.saldo
        saldo_excedido = valor > saldo

        if saldo_excedido:
            print("\nSaldo insuficiente!")

        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso")
            return True
        else:
            print("O valor inserido é inválido")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\nValor depositado com sucesso!")
        else:
            print("\n Valor inválido")
            return False
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, "0001", cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self._historico.transacoes
             if transacao["tipo"] == Saque.__name__]
        )

        limite_excedido = valor > self.limite
        saque_excedido = numero_saques >= self.limite_saques

        if limite_excedido:
            print("\nO valor do saque excedeu o limite!")

        elif saque_excedido:
            print("\nQuantia máxima de saques foi excedida!")

        else:
            resultado = super().sacar(valor)
            if resultado:
                self._historico.adicionar_transacao(Saque(valor))
            return resultado
        return False

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta._historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta._historico.adicionar_transacao(self)

cliente = PessoaFisica(
    cpf="12345678900",
    nome="Gabriel Grécia",
    data_nascimento="2000-01-01",
    endereco="Rua Exemplo, 123"
)

conta = ContaCorrente(numero=1, cliente=cliente)
cliente.adicionar_conta(conta)

deposito = Deposito(1000)
cliente.realizar_transacao(conta, deposito)

saque = Saque(300)
cliente.realizar_transacao(conta, saque)

print("Saldo atual:", conta.saldo)
print("Transações:")
for t in conta._historico.transacoes:
    print(t)
