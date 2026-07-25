import socket
import threading
import sys

def receive_messages(client_socket):
    """Continuously receives messages broadcasted from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == "NICKNAME_REQ":
                client_socket.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("\n❌ Lost connection to the server!")
            client_socket.close()
            sys.exit()

def send_messages(client_socket):
    """Handles outgoing user messages."""
    while True:
        try:
            msg = input()
            if msg.strip().lower() == '/exit':
                client_socket.close()
                print("👋 Logged out successfully.")
                sys.exit()
            
            formatted_msg = f"{nickname}: {msg}"
            client_socket.send(formatted_msg.encode('utf-8'))
        except:
            break

if __name__ == "__main__":
    print("=== LAN Text Chat Application ===")
    server_ip = input("Enter Server IP Address: ").strip()
    nickname = input("Choose your Nickname: ").strip()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((server_ip, 5000))
    except Exception as e:
        print(f"❌ Failed to connect to server: {e}")
        sys.exit()

    # Create distinct threads for receiving and sending to avoid blocking user input
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.daemon = True
    receive_thread.start()

    send_messages(client)