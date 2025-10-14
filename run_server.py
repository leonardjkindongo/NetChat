"""
Launcher script for the TCP chat server.
Run this from the project root:
    python run_server.py
"""

from server.server import receive_connections  # import the main server function

if __name__ == "__main__":
    receive_connections()
