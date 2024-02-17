import socket
import threading

def client_handler(client_socket, client_address, all_clients):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Received message from {client_address}: {message}")
                broadcast_message = f"{client_address}: {message}"
                for client in all_clients:
                    if client is not client_socket:
                        try:
                            client.send(broadcast_message.encode('utf-8'))
                        except:
                            client.close()
                            all_clients.remove(client)
        except:
            client_socket.close()
            all_clients.remove(client_socket)
            break

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server listening on port", port)
    
    all_clients = []

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        all_clients.append(client_socket)
        thread = threading.Thread(target=client_handler, args=(client_socket, client_address, all_clients,))
        thread.start()

if __name__ == "__main__":
    start_server('0.0.0.0', 5000)
