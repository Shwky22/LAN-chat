import socket
import threading

# Server Configurations (Listens on all available network interfaces)
HOST = '0.0.0.0'
PORT = 5000

# Lists to track connected clients and their nicknames
clients = []
nicknames = []

def broadcast(message):
    """Relays a message to all connected clients."""
    for client in clients:
        try:
            client.send(message)
        except:
            # Handle broken connection
            remove_client(client)

def remove_client(client):
    """Removes a client from active lists and closes its socket connection."""
    if client in clients:
        index = clients.index(client)
        nickname = nicknames[index]
        clients.remove(client)
        nicknames.remove(nickname)
        client.close()
        broadcast(f"📢 [{nickname}] has left the chat.".encode('utf-8'))
        print(f"[-] Disconnected: {nickname}")

def handle_client(client):
    """Handles continuous incoming messages from a specific client."""
    while True:
        try:
            message = client.recv(1024)
            if message:
                broadcast(message)
            else:
                remove_client(client)
                break
        except:
            remove_client(client)
            break

def receive_connections():
    """Main loop to listen for and accept new client connections."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Allows immediate port reuse upon restart
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    print(f"🚀 Server running and listening on port {PORT}...")
    print("⏳ Waiting for LAN connections...\n")

    while True:
        client, address = server.accept()
        print(f"[+] New connection from {address[0]}:{address[1]}")

        # Request client nickname upon initial connection
        client.send("NICKNAME_REQ".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        nicknames.append(nickname)
        clients.append(client)

        print(f"👤 Nickname registered: {nickname}")
        broadcast(f"🎉 [{nickname}] joined the chat!".encode('utf-8'))
        client.send("✅ Successfully connected to the server!\n".encode('utf-8'))

        # Spawn a dedicated thread per connected client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    try:
        receive_connections()
    except KeyboardInterrupt:
        print("\n🛑 Server shutting down.")