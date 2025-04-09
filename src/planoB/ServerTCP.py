import socket
import json
import carbone_sdk

csdk = carbone_sdk.CarboneSDK("test_eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIxMTMwNTQwNDc3MjQ3OTk1OTk4IiwiYXVkIjoiY2FyYm9uZSIsImV4cCI6MjQwNjQ4NjEyOCwiZGF0YSI6eyJ0eXBlIjoidGVzdCJ9fQ.AYIinvkaYLhjAnM92Aj0tlbyiW1EQVWbg4SdFgrgMCk8evHlSjav7AiXYcFU6QMTrk3zjmGjocWL3Pk6CH106_61AWzrCufXuRaF9ZpmPD6riQWw71jIUxXicrCIOFbPDuRpdLpqyc-wG1Srbuoce0-rdjMdmEUeJa7ocp6PgZvVvB0B")

template_path = "./template.docx"


TCP_IP = '127.0.0.1' # endereço IP do servidor
TCP_PORTA = 32336 # porta disponibilizada pelo servidor dessa máquina
TAMANHO_BUFFER = 1024

#Criação de socket TCP
# SOCK_STREAM, indica que será TCP.
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP e porta que o servidor deve aguardar a conexão
servidor.bind((TCP_IP, TCP_PORTA))

#Define o limite de conexões.
servidor.listen(1)

print(f"Server avaliable at {TCP_PORTA}.....")

# Aceita conexão
conn, addrReceived = servidor.accept()
print ('Connected address:', addrReceived)
while 1:
    #dados retidados da mensagem recebida
    dataReceived = conn.recv(TAMANHO_BUFFER)
    if dataReceived:
        print ("Received message:", dataReceived)
        if dataReceived == b"QUIT":
            conn.sendall("QUIT".encode('utf-8'))
            print("Chat closed")
            break
        try:
            icms = 0.2
            dados_cliente = json.loads(dataReceived.decode('utf-8'))
            nomeEmp = dados_cliente['nome']
            endereco = dados_cliente['endereco']
            dataFat = dados_cliente['data']
            ativos = dados_cliente['ativos']

            json_data = {

                "data": {
                    "nomeEmp": nomeEmp,
                    "endereco": endereco,
                    "dataFat": dataFat,
                    "ativos": ativos
                },
                "convertTo": "pdf"

            }
            report_bytes, unique_report_name = csdk.render(template_path, json_data)
        except Exception as e:
            print(f"Erro ao processar os dados: {e}")

        # envia mensagem para servidor
        MENSAGEM = input("Type server answer message: ")
        conn.sendall(MENSAGEM.encode('utf-8'))  # envia dados recebidos em letra maiuscula

