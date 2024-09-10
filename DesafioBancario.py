import re
from datetime import datetime

print("------------------------------------------------------------")
print('|    Desafio: Criando um sistema bancário                  |')
print("|                                                          |")
print("|    Autor: Felipe Alves da Silva                          |")
print("|    Data de criação: 04/09/2024                           |")
print("|    Perfil DIO: https://dio.me/users/felipe_alvessilva    |")
print("|    Github: https://github.com/felipealvss                |")
print("|    LinkedIn: https://www.linkedin.com/in/felipealvss/    |")
print("------------------------------------------------------------")


# Parametros iniciais
saldo_total = 0.00;
saque_diario = 3;
limite_saque = 500.00;
id_acao = 0;
audit = [];
id_agencia = 1;
agencia = f"{id_agencia:04}";
id_usuario = 0;
lista_usuario = [];
id_conta_corrente = 1;
lista_conta_corrente = [];


# Funcoes
import re

def criar_usuario(nome_usuario, data_nasc, cpf_cnpj, endereco):
    global id_usuario
    global lista_usuario

    aj_cpf_cnpj = re.sub(r'\D', '', cpf_cnpj)

    # Verificar se o CPF já está cadastrado
    for l in lista_usuario:
        if l['cpf_cnpj'] == aj_cpf_cnpj:
            return -1

    # Se o CPF não estiver na lista, adicionar o novo usuário
    id_user = id_usuario

    novo_usuario = {
        "id": id_usuario,
        "nome_usuario": nome_usuario,
        "data_nascimento": data_nasc,
        "cpf_cnpj": aj_cpf_cnpj,
        "endereco": endereco
    }
    
    lista_usuario.append(novo_usuario)
    id_usuario += 1

    return id_user, nome_usuario

def exibir_cadastros(lista_usuario):
    for l in lista_usuario:
        print(f"ID {l['id']} - Usuario: {l['nome_usuario']} - CPF: {l['cpf_cnpj']}")

def exibir_conta_corrente(lista_conta_corrente):
    for l in lista_conta_corrente:
        print(f"Conta: {l['numero_conta']} - Agencia: {agencia} - Usuario: {l['nome_usuario']}")

def criar_conta_corrente(agencia, usuario):
    global id_conta_corrente
    global lista_conta_corrente
    
    id_current_account = id_conta_corrente
    
    lista_conta_corrente.append({
        "numero_conta": id_current_account,
        "agencia": agencia,
        "nome_usuario": usuario
    })

    id_conta_corrente += 1

    return id_current_account

def deposito(id_, valor, /):
    
    global saldo_total
    global audit
    global id_acao
    global lista_usuario

    acao = 'DEPOSITO'
    saldo_total += valor
    id_acao += 1

    audit.append({
            'usuario': lista_usuario[id_]['nome_usuario'],
            'id': id_acao,
            'acao': acao,
            'valor': valor,
            'saldo': saldo_total
        })

    return acao, saldo_total

def saque(id_, valor):
    
    global saldo_total
    global saque_diario
    global limite_saque
    global id_acao
    global audit
    global lista_usuario

    acao = 'SAQUE'
    acao_fail = -1
    saldo_atual = saldo_total
    saldo_atual = saldo_total - valor

    if saldo_atual <= 0:
        return acao_fail, f'Operação cancelada! Saldo disponível: R$ {saldo_total:.2f}'
    elif saldo_atual > 0 and saque_diario < 1:
        return acao_fail, f'Operação cancelada! Quantidade de saques diarios disponíveis: {saque_diario}'
    elif saldo_atual > 0 and saque_diario > 0 and valor > limite_saque:
        return acao_fail, f'Operação cancelada! Valor de saque ultrapassa limite permitido (R$ {limite_saque:.2f})'
    elif saldo_atual > 0 and saque_diario > 0 and valor <= limite_saque:

        saldo_total -= valor
        saque_diario -= 1
        id_acao += 1

        audit.append({
            'usuario': lista_usuario[id_]['nome_usuario'],
            'id': id_acao,
            'acao': acao,
            'valor': valor,
            'saldo': saldo_total
        })

        return acao, saldo_total
    else:
        return acao_fail, -1

def extrato(id_, audit):
    data_geracao = datetime.now()
    data_geracao = data_geracao.strftime('%d/%m/%Y %H:%M:%S')

    print("-" * 45)
    print('---------     Extrato bancário:     ---------')
    print("")
    print(f"Data/Hora extrato: {data_geracao}")
    print(f'Usuário: {lista_usuario[id_]['nome_usuario']}')
    print(f'Agencia: {agencia}')
    print("")

    for a in audit:
        print(f"ID: {a['id']}")
        print(f"Ação: {a['acao']}")
        print(f"Valor informado: {a['valor']}")
        print(f"Saldo após operação: {a['saldo']}")
        print(" " * 40)
    
    print(f'Saldo total: {saldo_total}')
    print("-" * 45)

def final():
    print('\nFim de execução. Até a próxima!')

def opcoes():
    print("")
    print('Digite o número da opção você deseja realizar:')
    print('  1 - Depósito')
    print('  2 - Saque')
    print('  3 - Extrato')
    print('  4 - Encerrar')
    print("")



# Programa principal
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

while True:
    try:
        ret_cadastro = criar_usuario(nome_usuario=nome, data_nasc=dt_nasc, cpf_cnpj=cpf, endereco=endereco)
        
        if ret_cadastro[0] != -1:
            break
        else:
            n_cpf = input('CPF já cadastrado. Insira um documento válido: ')
            cpf = n_cpf
    except:
        n_cpf = input('CPF já cadastrado. Insira um documento válido: ')
        cpf = n_cpf

nome_completo = nome.split()

print(f'\nCadastro realizado, {nome_completo[0]}!')
print("=======================================================")
print(f'Para realizar transações, preciso que vincule seu cadastro a uma conta corrente.')

print(f'\nSelecionar um ID de usuário para associar a conta corrente: ')
exibir_cadastros(lista_usuario=lista_usuario)

selecionar_conta = input('Informar ID: ')

criar_conta_corrente(1, ret_cadastro[1])
print(f'\nConta corrente criada com sucesso.')
exibir_conta_corrente(lista_conta_corrente=lista_conta_corrente)
print("=======================================================")
print(f'\nSeguem abaixo as opções disponíveis.')

while True:

    opcoes()
    valor_operacao = 0.0

    while True:
        try:
            opcao = int(input('Opção: '))
            if opcao in (1,2,3,4):
                break
            else:
                print('Selecione uma opção válida!')
        except:
            print('Selecione uma opção da lista informada!')

    if opcao == 1: # Deposito
        print('\nOperação selecionada: Depósito')
        valor_operacao = float(input("Informe o valor R$ para depositar: R$ "))
        
        resultado = deposito(ret_cadastro, valor_operacao)
        
        print(f'\nOperação realizada.\nValor de depósito realizado: {resultado[1]:.2f}')
        print('')
        
        continuar = input('Continuar? [S/N]: ')
        
        if continuar == 'S':
            continue
        else:
            break
    elif opcao == 2: # Saque
        print('\nOperação selecionada: Saque')
        valor_operacao = float(input("Informe o valor R$ para sacar: R$ "))

        resultado = saque(id_=ret_cadastro, valor=valor_operacao)
        
        if resultado[0] == -1:
            print(resultado[1])
        else:
            print(f'\nOperação realizada.\nSaque realizado: {valor_operacao:.2f}\nValor de saldo atualizado: {resultado[1]:.2f}')
            print(f'Saques diários disponíveis: {saque_diario}')
            print('')
        
        continuar = input('Continuar? [S/N]: ')
        
        if continuar == 'S':
            continue
        else:
            break
    elif opcao == 3: # Extrato
        extrato(ret_cadastro[0], audit)
        print('')
        continuar = input('Continuar? [S/N]: ')
        
        if continuar == 'S':
            continue
        else:
            break    
    else:
        break

final()
