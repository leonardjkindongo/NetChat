import socket
import threading
from server.config import HOST, PORT, BUFFER_SIZE, ENCODING
from server.utils import format_message, log_event

# Create a TCP socket for the server
# AF_INET = IPv4, SOCK_STREAM = TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the specified host and port
server.bind((HOST, PORT))

# Start listening for incoming connections (max 5 waiting)
server.listen(5)

# Store connected clients and their usernames
clients = []
usernames = []

def broadcast(message: bytes, sender_client=None):
    """
    Send a message to all connected clients except the sender.
    """
    for client in clients:
        if client != sender_client:
            try:
                client.send(message)
            except:
                # Remove client if sending fails
                client.close()
                if client in clients:
                    clients.remove(client)

def handle_client(client):
    """
    Handle messages from a single connected client.
    Runs in a separate thread for each user.
    """
    while True:
        try:
            # Receive message from the client
            msg = client.recv(BUFFER_SIZE)
            if not msg:
                break  # client disconnected

            # Get username and format message
            username = usernames[clients.index(client)]
            formatted = format_message(username, msg.decode(ENCODING))

            # Print to server console
            print(formatted)

            # Broadcast to all other connected clients
            broadcast(formatted.encode(ENCODING), client)

        except:
            # Handle disconnection or crash
            index = clients.index(client)
            username = usernames[index]

            clients.remove(client)
            usernames.remove(username)
            client.close()

            log_event(f"{username} disconnected.")
            broadcast(f"{username} has left the chat.".encode(ENCODING))
            break

def receive_connections():
    """
    Accept incoming client connections and start a thread for each.
    """
    log_event(f"Server running on {HOST}:{PORT}")

    while True:
        # Wait for a new client to connect
        client, address = server.accept()
        log_event(f"Connection established with {address}")

        # Ask for username
        client.send("USERNAME".encode(ENCODING))
        username = client.recv(BUFFER_SIZE).decode(ENCODING)

        # Save username and client
        usernames.append(username)
        clients.append(client)

        log_event(f"{username} joined the chat.")
        broadcast(f"{username} joined the chat!".encode(ENCODING))

        # Confirm connection
        client.send("Connected to the chat server!".encode(ENCODING))

        # Start a new thread for this client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

# Run the server
if __name__ == "__main__":
    receive_connections()
