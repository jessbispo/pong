import socket #importa modulo socket

TCP_IP = '192.168.15.59' # endereço IP do servidor
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

        # envia mensagem para servidor
        MENSAGEM = input("Type server answer message: ")
        conn.sendall(MENSAGEM.encode('utf-8'))  # envia dados recebidos em letra maiuscula

