import socket #importa modulo socket

TCP_IP = '192.168.15.59' # endereço IP do servidor
TCP_PORTA_SERVER = 32336 # porta disponibilizada pelo servidor dessa máquina
TAMANHO_BUFFER = 1024


# Criação de socket TCP do cliente
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Conecta ao servidor em IP e porta especifica
cliente.connect((TCP_IP, TCP_PORTA_SERVER))

# envia mensagem para servidor
cliente.send("aa".encode('utf-8'))

while 1:
    # recebe dados do servidor
    dataReceived, addr = cliente.recvfrom(1024)
    if dataReceived:
        print ("Received message:", dataReceived)
        if dataReceived == b"QUIT":
            cliente.send("QUIT".encode('UTF-8'))
            print("Chat closed")
            break

        # envia mensagem para servidor
        MENSAGEM = input("Type your message for server: ")
        cliente.send(MENSAGEM.encode('UTF-8'))

# fecha conexão com servidor
cliente.close()


