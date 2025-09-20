class Cliente:
    def __init__(self, nome: str, cpf: str, endereco: str):
        self.nome = nome
        self.cpf = cpf
        self.endereco = endereco

    def __str__(self):
        return f"Cliente: {self.nome} | CPF: {self.cpf} | Endereço: {self.endereco}"


class ContaBancaria:
    _contador_contas = 1000  # número inicial de contas

    def __init__(self, cliente: Cliente, saldo_inicial: float = 0.0):
        self.numero = ContaBancaria._contador_contas
        ContaBancaria._contador_contas += 1
        self.saldo = saldo_inicial
        self.cliente = cliente

    def depositar(self, valor: float):
        if valor > 0:
            self.saldo += valor
            print(f"Depósito de R${valor:.2f} realizado com sucesso!")
        else:
            print("Valor inválido para depósito.")

    def sacar(self, valor: float):
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            print(f"Saque de R${valor:.2f} realizado com sucesso!")
        else:
            print("Saldo insuficiente ou valor inválido.")

    def transferir(self, conta_destino, valor: float):
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            conta_destino.depositar(valor)
            print(f"Transferência de R${valor:.2f} realizada para conta {conta_destino.numero}.")
        else:
            print("Transferência não realizada. Verifique o saldo ou valor.")

    def __str__(self):
        return f"Conta Nº: {self.numero} | Cliente: {self.cliente.nome} | Saldo: R${self.saldo:.2f}"


class Banco:
    def __init__(self, nome: str):
        self.nome = nome
        self.contas = []

    def adicionar_conta(self, conta: ContaBancaria):
        self.contas.append(conta)
        print(f"Conta {conta.numero} adicionada ao banco {self.nome}.")

    def buscar_conta(self, numero: int):
        for conta in self.contas:
            if conta.numero == numero:
                return conta
        print("Conta não encontrada.")
        return None

    def listar_contas(self):
        print(f"\nContas registradas no banco {self.nome}:")
        for conta in self.contas:
            print(conta)


# ----------------- EXEMPLO DE USO -----------------
if __name__ == "__main__":
    # Criando clientes
    cliente1 = Cliente("Maria Silva", "123.456.789-00", "Rua A, 123")
    cliente2 = Cliente("João Souza", "987.654.321-00", "Rua B, 456")

    # Criando contas
    conta1 = ContaBancaria(cliente1, 1000.0)
    conta2 = ContaBancaria(cliente2, 500.0)

    # Criando banco e adicionando contas
    banco = Banco("Banco Comunitário")
    banco.adicionar_conta(conta1)
    banco.adicionar_conta(conta2)

    # Operações
    conta1.depositar(200)
    conta1.sacar(150)
    conta1.transferir(conta2, 300)

    # Listando contas
    banco.listar_contas()
