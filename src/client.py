import pygame
import socket
import pickle

# Configurações do cliente
HOST = '127.0.0.1'
PORT = 12345

# Inicialização do pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    
    player = input("Qual jogador você é? ('left' ou 'right'): ")
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client_socket.close()
                pygame.quit()
                return
            
            # Envia os movimentos para o servidor
            if event.type == pygame.KEYDOWN:
                movement = 0
                if event.key == pygame.K_UP:
                    movement = -10
                elif event.key == pygame.K_DOWN:
                    movement = 10
                
                client_socket.sendall(pickle.dumps({'player': player, 'movement': movement}))
        
        # Recebe o estado atualizado do servidor
        game_state = pickle.loads(client_socket.recv(1024))
        
        # Desenha as raquetes com base no estado recebido
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 0, 0), (50, game_state['left_paddle'], 10, 100))
        pygame.draw.rect(screen, (0, 0, 255), (740, game_state['right_paddle'], 10, 100))
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
