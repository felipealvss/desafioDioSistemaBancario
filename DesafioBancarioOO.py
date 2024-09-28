import re
from datetime import datetime
from abc import ABC, abstractmethod

print("------------------------------------------------------------")
print('|  Desafio: Criando um sistema bancário - Utilizando POO   |')
print("|                                                          |")
print("|    Autor: Felipe Alves da Silva                          |")
print("|    Data de criação: 28/09/2024                           |")
print("|    Perfil DIO: https://dio.me/users/felipe_alvessilva    |")
print("|    Github: https://github.com/felipealvss                |")
print("|    LinkedIn: https://www.linkedin.com/in/felipealvss/    |")
print("------------------------------------------------------------")

### Definição de classes
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @property
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self._valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self._valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}' for chave, valor in self.__dict__.items()])}"

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}' for chave, valor in self.__dict__.items()])}"

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data_acao": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            })

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def historico(self):
        return self._historico

    def sacar(self, valor: float):
        if valor > self._saldo:
            return '-saldo_insuf'
        elif valor > 0:
            self._saldo -= valor
        else:
            return '-valor_incor'

        return True

    def depositar(self, valor: float):
        if valor > 0:
            self._saldo += valor
        else:
            return '-valor_incor'

        return True

    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}' for chave, valor in self.__dict__.items()])}"

class ContaCorrente(Conta):
    def __init__(self, numero, cliente):
        super().__init__(numero, cliente)
        self._limite = 500
        self._limite_diario = 3

    def sacar(self, valor: float):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )
        if valor > self._limite:
            return 'limit_exced'
        elif numero_saques >= self._limite_diario:
            return 'quant_expir'
        else:
            return super().sacar(valor)

### Funções gerais
def final():
    print('\nFim de execução. Até a próxima!')

def opcoes():
    print("")
    print('Digite o número da opção que você deseja realizar:')
    print('  1 - Depósito')
    print('  2 - Saque')
    print('  3 - Extrato')
    print('  4 - Encerrar')
    print("")

def exibir_extrato(cliente):
    print("-" * 45)
    print('---------     Extrato bancário:     ---------')
    print(f'Usuário: {cliente._nome}')
    print(f'Agencia: 0001')
    print("")

    for transacao in cliente._contas[0].historico.transacoes:
        print(f"Tipo: {transacao['tipo']}")
        print(f"Valor: {transacao['valor']}")
        print(f"Data/Hora: {transacao['data_acao']}")
        print(" " * 40)
    
    print(f'Saldo total: {cliente._contas[0].saldo}')
    print("-" * 45)

### Programa principal
if __name__ == "__main__":
    print("")
    print("=======================================================")
    print("              SISTEMA BANCÁRIO TESTE D.I.O             ")
    print("=======================================================")
    print("")

    print(f'Olá, querido(a) cliente!\nPara seguirmos, preciso que faça o cadastro a seguir:\n')

    nome = input("Informe seu nome: ")
    dt_nasc = input("Informe sua data de nascimento (Exemplo: 01/01/2001): ")
    cpf = input("Informe seu CPF: ")

    print("Agora preciso de dados de localização.\n(Logradouro - Nr. da residência - Bairro - Cidade - Sigla de estado)\n")

    logradouro = input("Informe seu logradouro: ")
    nro_residencia = input("Informe seu nr. da residência: ")
    bairro = input("Informe seu bairro: ")
    cidade = input("Informe sua cidade: ")
    sigla_estado = input("Informe a sigla do seu estado: ")

    endereco = f'{logradouro} - {nro_residencia} - {bairro} - {cidade} - {sigla_estado}'

    print('\nEnviando dados para cadastro...')
    
    cliente = PessoaFisica(endereco, cpf, nome, dt_nasc)
    conta = ContaCorrente(1, cliente)
    cliente.adicionar_conta(conta)

    print(f'\nCadastro realizado, {nome.split()[0]}! Conta corrente criada com sucesso.')

    while True:
        opcoes()

        while True:
            try:
                opcao = int(input('Opção: '))
                if opcao in (1, 2, 3, 4):
                    break
                else:
                    print('Selecione uma opção válida!')
            except ValueError:
                print('Selecione uma opção da lista informada!')

        if opcao == 1:  # Depósito
            valor_operacao = float(input("Informe o valor R$ para depositar: R$ "))
            transacao = Deposito(valor_operacao)
            cliente.realizar_transacao(conta, transacao)
            print(f'\nDepósito realizado com sucesso! Valor depositado: R$ {valor_operacao:.2f}')
        
        elif opcao == 2:  # Saque
            valor_operacao = float(input("Informe o valor R$ para sacar: R$ "))
            transacao = Saque(valor_operacao)
            resultado = cliente.realizar_transacao(conta, transacao)

            if resultado == '-saldo_insuf':
                print('Operação cancelada! Saldo insuficiente.')
            elif resultado == '-valor_incor':
                print('Operação cancelada! Valor de saque inválido.')
            else:
                print(f'\nSaque realizado com sucesso! Valor sacado: R$ {valor_operacao:.2f}')

        elif opcao == 3:  # Extrato
            exibir_extrato(cliente)
        
        else:  # Encerrar
            final()
            break
