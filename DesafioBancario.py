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
id_acao = 0
audit = []



# Funcoes
def deposito(valor):
    
    global saldo_total
    global audit
    global id_acao

    acao = 'DEPOSITO'
    saldo_total += valor
    id_acao += 1

    audit.append({
            'id': id_acao,
            'acao': acao,
            'valor': valor,
            'saldo': saldo_total
        })

    return acao, saldo_total

def saque(valor):
    
    global saldo_total
    global saque_diario
    global limite_saque
    global id_acao
    global audit

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
            'id': id_acao,
            'acao': acao,
            'valor': valor,
            'saldo': saldo_total
        })

        return acao, saldo_total
    else:
        return acao_fail, -1

def extrato(audit):
    data_geracao = datetime.now()
    data_geracao = data_geracao.strftime('%d/%m/%Y %H:%M:%S')

    print("-" * 45)
    print('---------     Extrato bancário:     ---------')
    print("")
    print(f"Data/Hora extrato: {data_geracao}")
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
    print('Fim de execução. Até a próxima!')

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
        
        resultado = deposito(valor_operacao)
        
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

        resultado = saque(valor_operacao)
        
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
        extrato(audit)
        print('')
        continuar = input('Continuar? [S/N]: ')
        
        if continuar == 'S':
            continue
        else:
            break    
    else:
        break

final()
