import socket
import threading
from datetime import datetime
from colorama import Fore
import argparse


pr = argparse.ArgumentParser()
pr.add_argument('--host', type=str, required=True)
pr.add_argument('--port', type=int, required=True)
args = pr.parse_args()

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((args.host,args.port))
server.listen(5)    #max connection listening : 5

clients = []        #client list
nicknames = []      #nicknames list
def broadcast(data):
    for x in clients:
        x.send(data.encode("utf-8"))

def rcv_send(client,addr):
    while True:
        try:
            data_x = client.recv(1024).decode("utf-8")
            broadcast(data_x)
        except:
            print(Fore.RED + f"{client} / {addr} - disconnected")
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat !")
            nicknames.remove(nickname)
            Fore.RESET
            break



def accept_conn():
    while True:
        client, addr = server.accept()
        print(Fore.GREEN + f"Got connection from {str(client)}")
        Fore.RESET
        client.send("Username".encode("utf-8"))
        user_nick = client.recv(1024).decode("utf-8")
        nicknames.append(user_nick)
        clients.append(client)
        for z in clients:
            check = z.send(f"{user_nick} joined to chat".encode("utf-8"))

        thread_receive = threading.Thread(target=rcv_send,args=(client,addr))
        thread_receive.start()


print(Fore.BLUE + f"Server started and listening on {args.host}:{args.port}")
now = datetime.now()
start_time = now.strftime("%H:%M:%S")
print(Fore.BLUE + f"Server start time {start_time}")
Fore.RESET
accept_conn()