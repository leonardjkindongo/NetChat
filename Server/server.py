import socket          # For creating TCP sockets
import threading       # For handling multiple clients concurrently
from Server.config import HOST, PORT, BUFFER_SIZE, ENCODING  # Server configuration
from Server.utils import format_message, log_event          # Helper functions

# -----------------------------
# Global lists to track clients
# -----------------------------
clients = []    # List of connected client sockets
usernames = []  # Corresponding usernames of connected clients

# -----------------------------
# Function to broadcast messages
# -----------------------------
def broadcast(message: bytes, sender_client=None):
    """
    Send a message to all connected clients except the sender.
    
    Args:
        message (bytes): The message to send.
        sender_client (socket, optional): The client who sent the message. Default None.
    """
    for client in clients:
        if client != sender_client:  # Skip the sender
            try:
                client.send(message)  # Send the message
            except:
                # If sending fails, remove client
                client.close()
                if client in clients:
                    clients.remove(client)

# -----------------------------
# Function to handle a single client
# -----------------------------
def handle_client(client):
    """
    Handle communication with a connected client.
    Runs in a separate thread for each client.
    
    Args:
        client (socket): The client socket to handle.
    """
    while True:
        try:
            # Receive message from client
            msg = client.recv(BUFFER_SIZE)
            
            if not msg:
                # Client disconnected
                break

            # Get username of the sender
            username = usernames[clients.index(client)]
            
            # Format message with timestamp and username
            formatted = format_message(username, msg.decode(ENCODING))
            
            # Print message to server console
            print(formatted)
            
            # Broadcast to other clients
            broadcast(formatted.encode(ENCODING), client)

        except:
            # Handle client disconnection or crash
            if client in clients:
                index = clients.index(client)
                username = usernames[index]

                clients.remove(client)
                usernames.remove(username)
                client.close()

                log_event(f"{username} disconnected.")
                broadcast(f"{username} has left the chat.".encode(ENCODING))
            break

# -----------------------------
# Main server function
# -----------------------------
def main():
    """
    Main function to start the TCP chat server.
    Accepts incoming connections and starts a thread for each client.
    """
    # Create TCP socket
    # AF_INET = IPv4, SOCK_STREAM = TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind socket to host and port
    server.bind((HOST, PORT))

    # Start listening for incoming connections (max 5 queued)
    server.listen(5)

    log_event(f"Server running on {HOST}:{PORT}")

    while True:
        # Accept a new client connection
        client, address = server.accept()
        log_event(f"Connection established with {address}")

        # Ask client for username
        client.send("USERNAME".encode(ENCODING))
        username = client.recv(BUFFER_SIZE).decode(ENCODING)

        # Save username and client socket
        usernames.append(username)
        clients.append(client)

        # Notify server and other clients
        log_event(f"{username} joined the chat.")
        broadcast(f"{username} joined the chat!".encode(ENCODING))

        # Confirm connection to the client
        client.send("Connected to the chat server!".encode(ENCODING))

        # Start a new thread to handle this client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

# -----------------------------
# Allows running server.py directly
# -----------------------------
if __name__ == "__main__":
    main()
