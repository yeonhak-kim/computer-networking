from ipaddress import ip_address
from re import L
import socket
import select
import threading
import sys 
import argparse
import datetime

#TODO: Implement all code for your server here

# Use sys.stdout.flush() after print statemtents


# initialize parser for command-line inputs
parser = argparse.ArgumentParser(description="multi-user chat server")
parser.add_argument("-start", dest="start", default=True, required=True, action="store_true", help="start server")
parser.add_argument("-port", dest="port", default=None, type=int, required=True, help="server port number")
parser.add_argument("-passcode", dest="passcode", type=str, default=None, required=True, help="required passcode for joining the chat room")
args = parser.parse_args()

# set hostname, server port number, and passcode
host= "127.0.0.1"
server_port = args.port
server_passcode = args.passcode

# initialize server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, server_port))
server.listen(5)

# cache
clients = []
usernames = []
username_dict = set()

def broadcast(message):
    print(message.decode("utf-8"))
    sys.stdout.flush()
    for client in clients:
        try:
            client.send(message)
        except:
            client.close()
def handle(client):
    while True:
        try:
            # if client closed or error occurred, disconnect
            message = client.recv(1024)
            
            if message == "CONNECTION-CLOSE".encode("utf-8"):   
                # client remove
                index = clients.index(client)
                clients.remove(client)
                #client.shutdown(1)
                client.close()
                username = usernames[index]
                broadcast(f"{username} left the room.".encode("utf-8"))
                usernames.remove(username)
                username_dict.discard(username)
                sys.exit()
            else:  
                broadcast(message)
        except:
            # client remove
            if client not in clients:
                sys.exit()

            index = clients.index(client)
            clients.remove(client)
            #client.shutdown(1)
            client.close()
            username = usernames[index]
            broadcast(f"{username} left the room.".encode("utf-8"))
            usernames.remove(username)
            username_dict.discard(username)
            sys.exit()

def receive():
    print(f"Server started on port {server_port}. Accepting connections")
    sys.stdout.flush()
    #try:
    while True:
        client, address = server.accept()

        # connection established, notify client 
        client.send("CONNECTED".encode("utf-8"))

        # passcode validation check
        client_passcode = client.recv(1024).decode("utf-8")
        if (client_passcode == server_passcode) and (0 < len(client_passcode) <= 5):
            client.send("AUTHORIZED".encode("utf-8"))

        else:
            client.send("AUTH_FAIL".encode("utf-8"))
            client.close()

        # user validation check
        username = client.recv(1024).decode("utf-8")
        if (username in username_dict) or not (0 < len(username) <= 8):
            client.send("USER_INVALID".encode("utf-8"))
            client.close()

        # notify all clients on new client
        notification_msg = f"{username} joined the chatroom"
        broadcast(notification_msg.encode("utf-8"))

        # add new client to cache
        clients.append(client)
        usernames.append(username)
        username_dict.add(username)

        # notify client over successful connection
        client.send(f"Connected to {host} on port {server_port}".encode("utf-8"))

        # handle each client socket via threading
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

    #except KeyboardInterrupt:
    #    sys.exit()

    #except Exception as e:
    #    print("General Error: ", str(e))
    #    sys.exit()
receive()
#if __name__ == "__main__":
#	main(sys.argv[1:])
