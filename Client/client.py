import socket
import threading
from Client.config import HOST, PORT, BUFFER_SIZE, ENCODING  # Import configuration
from Client.utils import display_instructions  # Import helper function to show instructions

def main():
    """
    Main entry point for the TCP chat client.
    Connects to server, starts send/receive threads.
    """
    # -----------------------------
    # Create TCP client socket
    # -----------------------------
    # AF_INET = IPv4, SOCK_STREAM = TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Attempt to connect to the server
    try:
        client.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("❌ Unable to connect to the server. Make sure it’s running.")
        return  # Exit if connection fails

    # -----------------------------
    # Get username from user
    # -----------------------------
    username = input("Enter your username: ")

    # Show basic instructions for the chat
    display_instructions()

    # -----------------------------
    # Define message receiving thread
    # -----------------------------
    def receive_messages():
        """
        Continuously listen for messages from the server and print them.
        Runs in a separate thread so the user can type at the same time.
        """
        while True:
            try:
                # Receive a message from the server
                message = client.recv(BUFFER_SIZE).decode(ENCODING)

                if message == 'USERNAME':
                    # Server requests the username at connection time
                    client.send(username.encode(ENCODING))
                else:
                    # Display any other message (chat message, system info, etc.)
                    print(message)
            except:
                # If server disconnects or error occurs, exit the loop
                print("⚠️ Connection to the server was lost.")
                client.close()
                break

    # -----------------------------
    # Define message sending thread
    # -----------------------------
    def send_messages():
        """
        Continuously read user input and send messages to the server.
        """
        while True:
            message = input('')  # Read input from the user
            if message.lower() == 'quit':
                # If user types 'quit', close connection and exit
                client.close()
                break
            try:
                # Encode message and send to server
                client.send(message.encode(ENCODING))
            except:
                print("⚠️ Failed to send message. Connection may be closed.")
                break

    # -----------------------------
    # Start threads for send/receive
    # -----------------------------
    # Thread for receiving messages
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    # Thread for sending messages
    send_thread = threading.Thread(target=send_messages)
    send_thread.start()

    # Optional: wait for threads to finish
    receive_thread.join()
    send_thread.join()

# If this file is run directly (or via launcher), start main()
if __name__ == "__main__":
    main()
