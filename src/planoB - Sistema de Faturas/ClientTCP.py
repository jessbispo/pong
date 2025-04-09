import socket
import json
import time


def enviar_dados_energia():
    TCP_IP = '127.0.0.1'  # endereço IP Cliente
    TCP_PORTA_SERVER = 32336  # porta disponibilizada pelo servidor dessa máquina
    TAMANHO_BUFFER = 1024

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((TCP_IP, TCP_PORTA_SERVER))

    print("\n=== ANALISE DE ECONOMIA DE ENERGIA ===\n")

    # Coleta dados do cliente
    nome_cliente = input("Nome do cliente: ")
    endereco = input("Endereço: ")
    # ativos obrigatorios: nome, qtd, potencia e horas_uso
    ativos = []

    continuar = True
    while continuar:
        print("\n=== Adicionar ativo eletrico ===")
        nome_ativo = input("Nome do ativo (ex: Ar-condicionado, Geladeira): ")

        try:
            qtd = int(input("quantidade: "))
            potencia = float(input("potencia em watts: "))
            horas_uso = float(input("horas de uso diario: "))
        except ValueError:
            print("Erro: Por favor, insira valores numericos validos.")
            continue

        ativos.append({
            'nome': nome_ativo,
            'quantidade': qtd,
            'potencia': potencia,
            'horas_uso': horas_uso
        })

        opcao = input("\nDeseja adicionar outro ativo? (s/n): ")
        continuar = opcao.lower() == 's'

    # Prepara os dados para enviar
    dados = {
        'nome': nome_cliente,
        'endereco': endereco,
        'data': time.strftime("%d/%m/%Y"),
        'ativos': ativos
    }

    # Envia os dados para o servidor
    client.send(json.dumps(dados).encode('utf-8'))

    # Recebe a resposta do servidor
    resposta = client.recv(1024).decode('utf-8')

    if resposta == "ARQUIVO_PDF":

        client.send("PRONTO".encode('utf-8'))
        file_size = int(client.recv(1024).decode('utf-8'))
        client.send("OK".encode('utf-8'))

        # Recebe o arquivo
        pdf_data = b''
        bytes_recebidos = 0

        while bytes_recebidos < file_size:
            data = client.recv(4096)
            if not data:
                break
            pdf_data += data
            bytes_recebidos += len(data)

        pdf_path = f"pdfs/economia_energia_{nome_cliente.replace(' ', '_')}.pdf"
        with open(pdf_path, 'wb') as file:
            file.write(pdf_data)

        print(f"\nRelatorio salvo em: {pdf_path}")
    else:
        print(f"\nErro: {resposta}")

    client.close()


if __name__ == "__main__":
    try:
        enviar_dados_energia()
    except Exception as e:
        print(f"Erro: {e}")

    input("\nPressione Enter para sair...")