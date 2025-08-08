# Sistema Bancário - Versão 1

saldo = 0.0
limite_saque = 500.0
extrato = []
saques_diarios = 0
LIMITE_SAQUES_DIARIOS = 3

while True:
    print("\n=== MENU ===")
    print("[d] Depositar")
    print("[s] Sacar")
    print("[e] Extrato")
    print("[q] Sair")

    opcao = input("Escolha uma opção: ").lower()

    if opcao == "d":
        valor = float(input("Informe o valor para depósito: R$ "))
        if valor > 0:
            saldo += valor
            extrato.append(f"Depósito: R$ {valor:.2f}")
            print("✅ Depósito realizado com sucesso.")
        else:
            print("❌ Valor inválido. Só é permitido depositar valores positivos.")

    elif opcao == "s":
        if saques_diarios >= LIMITE_SAQUES_DIARIOS:
            print("❌ Limite diário de saques atingido.")
            continue

        valor = float(input("Informe o valor para saque: R$ "))
        if valor <= 0:
            print("❌ Valor inválido. Só é permitido sacar valores positivos.")
        elif valor > saldo:
            print("❌ Saldo insuficiente.")
        elif valor > limite_saque:
            print(f"❌ O limite por saque é de R$ {limite_saque:.2f}.")
        else:
            saldo -= valor
            extrato.append(f"Saque:    R$ {valor:.2f}")
            saques_diarios += 1
            print("✅ Saque realizado com sucesso.")

    elif opcao == "e":
        print("\n===== EXTRATO =====")
        if not extrato:
            print("Não foram realizadas movimentações.")
        else:
            for item in extrato:
                print(item)
        print(f"\nSaldo atual: R$ {saldo:.2f}")

    elif opcao == "q":
        print("Encerrando sistema... Obrigado por utilizar nosso banco!")
        break

    else:
        print("❌ Opção inválida. Tente novamente.")
