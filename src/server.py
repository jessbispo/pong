import socket
import pickle
from threading import Thread

# Configurações do servidor
HOST = '127.0.0.1'
PORT = 12345

# Estado inicial do jogo
game_state = {'left_paddle': 250, 'right_paddle': 250}

def handle_client(conn, addr):
    global game_state
    print(f"Conexão estabelecida com {addr}")
    while True:
        try:
            # Recebe os eventos de controle do cliente
            data = conn.recv(1024)
            if not data:
                break
            event = pickle.loads(data)
            if event['player'] == 'left':
                game_state['left_paddle'] += event['movement']
            elif event['player'] == 'right':
                game_state['right_paddle'] += event['movement']
            
            # Envia o estado atualizado do jogo para o cliente
            conn.sendall(pickle.dumps(game_state))
        except Exception as e:
            print(f"Erro: {e}")
            break
    conn.close()

# Criação do socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(2)
print("Aguardando conexões...")

while True:
    conn, addr = server_socket.accept()
    Thread(target=handle_client, args=(conn, addr)).start()
