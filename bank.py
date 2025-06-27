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
            "data": datetime.now()
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
            [t for t in self._historico.transacoes if t["tipo"] == "Saque"]
        )
        limite_excedido = valor > self.limite
        saque_excedido = numero_saques >= self.limite_saques

        if limite_excedido:
            print("\nO valor do saque excedeu o limite!")
        elif saque_excedido:
            print("\nQuantia máxima de saques foi excedida!")
        else:
            return super().sacar(valor)
        return False

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def executar(self, conta):
        pass

    def registrar(self, conta):
        hoje = datetime.now().date()
        transacoes_hoje = [
            t for t in conta._historico.transacoes
            if isinstance(t["data"], datetime) and t["data"].date() == hoje
        ]
        if len(transacoes_hoje) >= 10:
            print("\nLimite diário de transações atingido. Tente novamente amanhã.")
            return
        sucesso = self.executar(conta)
        if sucesso:
            conta._historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def executar(self, conta):
        return conta.sacar(self.valor)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def executar(self, conta):
        return conta.depositar(self.valor)

cliente = PessoaFisica(
    cpf="12345678900",
    nome="Gabriel Grécia",
    data_nascimento="2000-01-01",
    endereco="Rua Exemplo, 123"
)

conta = ContaCorrente(numero=1, cliente=cliente)
cliente.adicionar_conta(conta)

for i in range(12):
    deposito = Deposito(100)
    cliente.realizar_transacao(conta, deposito)

saque = Saque(50)
cliente.realizar_transacao(conta, saque)

print(f"\nSaldo atual: R${conta.saldo:.2f}")
print("\nTransações do dia:")
for t in conta._historico.transacoes:
    data_formatada = t["data"].strftime("%d/%m/%Y %H:%M:%S")
    print(f'{t["tipo"]} de R${t["valor"]:.2f} em {data_formatada}')
