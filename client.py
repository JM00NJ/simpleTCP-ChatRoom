import socket
import threading
from colorama import Fore
from datetime import datetime
import os
import argparse


pr = argparse.ArgumentParser()
pr.add_argument('--host', type=str, required=True)
pr.add_argument('--port', type=int, required=True)
args = pr.parse_args()


client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((args.host,args.port))

username = input("Set your nickname: ")

def receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "Username":
                client.send(username.encode("utf-8"))
            else:
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print(Fore.GREEN + current_time + "::" + message+"\n")
                Fore.RESET
                
        except KeyboardInterrupt:
            print(Fore.RED + "-Left the chat-")
            Fore.RESET
            client.close
            os._exit(0)
        except ConnectionResetError:
            print(Fore.RED + "Error 'Disconnected'")
            Fore.RESET
            client.close()
            os._exit(0)
        except:
            print(Fore.RED + "Got 'Unknown Error'")
            Fore.RESET
            os._exit(0)


def sendText():
    while True:
        try:
            message = f"{username} : {input("")}"
            client.send(message.encode("utf-8"))
        except KeyboardInterrupt:
            Fore.RESET
            os._exit(0)
        except EOFError:
            print("EOFError_Terminating")
            os._exit(0)
        except:
            os._exit(0)

receive_thread = threading.Thread(target=receive)
receive_thread.start()

sendText_thread = threading.Thread(target=sendText)
sendText_thread.start()