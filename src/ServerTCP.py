import socket
import pygame
from sys import exit

TCP_IP = '192.168.15.59' # endereço IP do servidor
TCP_PORTA = 32336 # porta disponibilizada pelo servidor dessa máquina
TAMANHO_BUFFER = 1024

#Criação de socket TCP
# SOCK_STREAM, indica que será TCP.
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP e porta que o servidor deve aguardar a conexão
servidor.bind((TCP_IP, TCP_PORTA))

#Define o limite de conexões.
servidor.listen(2)

pygame.init()
screen = pygame.display.set_mode((800, 400))

pygame.display.set_caption('Pong')
clock = pygame.time.Clock()

player_racket_1 = pygame.Surface((20,50))
player_racket_1.fill((238, 130, 238))
player_racket_2 = pygame.Surface((20,50))
player_racket_2.fill('Blue')

print(f"Server avaliable at {TCP_PORTA}.....")

# Aceita conexão
conn, addrReceived = servidor.accept()
print ('Connected address:', addrReceived)
print("Entrando no while")
while True:
    for event in pygame.event.get():
        print("To no evento")
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    print("N to no evento")
    #dados retidados da mensagem recebida
    # TODO Entender como receber movimentos do cliente(player)
    dataReceived = conn.recv(TAMANHO_BUFFER)
    if dataReceived:
        print ("Received message:", dataReceived)
        if dataReceived == b"QUIT":
            conn.sendall("QUIT".encode('utf-8'))
            print("Chat closed")
            break

    screen.blit(player_racket_1, (0,190))
    screen.blit(player_racket_2, (780,190))

    pygame.display.update()
    clock.tick(60)
