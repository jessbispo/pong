import socket
import json
import carbone_sdk
import random

#Contrutor do carbone SDK
csdk = carbone_sdk.CarboneSDK("test_eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIxMTMwNTQwNDc3MjQ3OTk1OTk4IiwiYXVkIjoiY2FyYm9uZSIsImV4cCI6MjQwNjQ4NjEyOCwiZGF0YSI6eyJ0eXBlIjoidGVzdCJ9fQ.AYIinvkaYLhjAnM92Aj0tlbyiW1EQVWbg4SdFgrgMCk8evHlSjav7AiXYcFU6QMTrk3zjmGjocWL3Pk6CH106_61AWzrCufXuRaF9ZpmPD6riQWw71jIUxXicrCIOFbPDuRpdLpqyc-wG1Srbuoce0-rdjMdmEUeJa7ocp6PgZvVvB0B")
# csdk = carbone_sdk.CarboneSDK() # Passe no terminal com export <test_api_token>

template_path = "../../docs/FATURA.docx"

TCP_IP = '127.0.0.1' # endereço IP do servidor
TCP_PORTA = 32336 # porta disponibilizada pelo servidor dessa máquina
TAMANHO_BUFFER = 1024

#Criação de socket TCP
# SOCK_STREAM, indica que será TCP.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP e porta que o server deve aguardar a conexão
server.bind((TCP_IP, TCP_PORTA))

#Define o limite de conexões.
server.listen(1)

print(f"Server avaliable at {TCP_PORTA}.....")

# Aceita conexão
conn, addrReceived = server.accept()
print ('Connected address:', addrReceived)
while 1:
    #dados retidados da mensagem recebida
    dataReceived = conn.recv(TAMANHO_BUFFER)
    if dataReceived:
        if dataReceived == b"QUIT":
            conn.sendall("QUIT".encode('utf-8'))
            print("Chat closed")
            break
        try:
            #Constantes
            icms = 0.2 #imposto
            pld_ne = 58.96 #taxa por receber energia de outra sub-regiao (ne = nordeste) no mercado livre
            custo_kwh_mr = 50.00 # gasto por kwh para comprar do mercado regulado
            custo_kwh_ml = 10.00 # gasto por kwh para comprar do mercado livre

            #Dados recebidos
            dados_cliente = json.loads(dataReceived.decode('utf-8'))
            nomeEmp = dados_cliente['nome']
            endereco = dados_cliente['endereco']
            dataFat = dados_cliente['data']
            ativos = dados_cliente['ativos']
            custo_por_ativo = []
            total_mr = 0
            total_ml = 0

            for ativo in ativos:
                gasto_atual = ativo['potencia'] * ativo['horas_uso'] * 0.03
                cstMR = gasto_atual * custo_kwh_mr * (1 + icms)
                cstML = gasto_atual * custo_kwh_ml * (1 + icms) + pld_ne
                total_mr += cstMR
                total_ml += cstML
                custo_por_ativo.append({
                    "nome": ativo['nome'],
                    "gasto": gasto_atual,
                    "cstMR": cstMR,
                    "cstML": cstML
                })
            percEc = (total_mr / total_ml) * 100

            json_data = {

                "data": {
                    "icms": icms,
                    "idFat": random.randint(100000000,999999999),
                    "nomeEmp": nomeEmp,
                    "endereco": endereco,
                    "dataFat": dataFat,
                    "atvs": custo_por_ativo,
                    "totalMR": total_mr,
                    "totalML": total_ml,
                    "percEc": percEc

                },
                "convertTo": "pdf"

            }
            report_bytes, unique_report_name = csdk.render(template_path, json_data)

            # Gera o documento pdf
            fd = open("../../docs/"+unique_report_name, "wb")
            fd.write(report_bytes)
            fd.close()


            conn.sendall("Fatura gerada!".encode('utf-8'))  # envia dados recebidos em letra maiuscula


        except Exception as e:
            print(f"Erro ao processar os dados: {e}")
            conn.sendall(f"Fatura nao foi gerada!".encode('utf-8'))  # envia dados recebidos em letra maiuscula



