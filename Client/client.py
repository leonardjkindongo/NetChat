import socket
import threading
from client.config import HOST, PORT, BUFFER_SIZE, ENCODING
from client.utils import display_instructions

# Create a TCP socket for the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client.connect((HOST, PORT))
except ConnectionRefusedError:
    print("❌ Unable to connect to the server. Make sure it’s running.")
    exit()

# Prompt for username
username = input("Enter your username: ")

# Show instructions
display_instructions()

def receive_messages():
    """
    Continuously receive and print messages from the server.
    Runs in a separate thread so the user can type while receiving.
    """
    while True:
        try:
            message = client.recv(BUFFER_SIZE).decode(ENCODING)

            if message == 'USERNAME':
                # Send username when the server requests it
                client.send(username.encode(ENCODING))
            else:
                # Print any other incoming messages
                print(message)
        except:
            # Connection lost or server closed
            print("⚠️ Connection to the server was lost.")
            client.close()
            break

def send_messages():
    """
    Continuously read user input and send messages to the server.
    """
    while True:
        message = input('')
        if message.lower() == 'quit':
            client.close()
            break
        client.send(message.encode(ENCODING))

# Start threads: one for receiving, one for sending
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
