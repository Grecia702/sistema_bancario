option = 1
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

def depositar_dinheiro(quantia, saldo, limite, extrato):
    if quantia > limite:
        print("Voce não tem essa quantia")
        return saldo, limite, extrato
    saldo += quantia
    limite -= quantia
    extrato += f"Depósito : R$ {quantia:.2f}\n"
    print(f"Quantia depositada! \nSaldo Atual: {saldo}\nLimite Atual: {limite}")
    return saldo, limite, extrato

def sacar_dinheiro(quantia, saldo, numero_saques, limite, extrato):
    if numero_saques >= LIMITE_SAQUES:
        print("Você atingiu o limite diário de saques!")
        return saldo, numero_saques
    if quantia > saldo:
        print("Saldo insuficiente!")
        return saldo, numero_saques
    saldo -= quantia
    limite += quantia
    numero_saques += 1
    extrato += f"Saque : R$ {quantia:.2f}\n"
    print(f"Quantia sacada! \nSaldo Atual: R$ {saldo}\nNumero de saques {numero_saques}")
    return saldo, numero_saques, extrato

def visualizar_extrato(extrato, limite, saldo):
    print(f"{extrato}\n----------------\n\nLimite Disponível: {limite}\nSaldo atual: R$ {saldo}")

while True:
    print("""
[1] - Depositar
[2] - Sacar
[3] - Visualizar extrato
[0] - Sair
""")

    option = int(input("Digite a opção: "))
    if option == 1:
        quantia = int(input("Digite a quantidade a depositar: "))
        saldo, limite, extrato = depositar_dinheiro(quantia, saldo, limite, extrato)
    elif option == 2:
        quantia = int(input("Digite a quantidade a sacar: "))
        saldo, numero_saques, extrato = sacar_dinheiro(quantia, saldo, numero_saques, limite, extrato)
    elif option == 3:
        visualizar_extrato(extrato, limite, saldo)
    elif option == 0:
        print("Saindo...")
        break
    else:
        print("Opção inválida.")