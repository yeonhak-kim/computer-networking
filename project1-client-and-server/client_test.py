import socket
import threading
import sys 
import argparse


#TODO: Implement a client that connects to your server to chat with other clients here

# Use sys.stdout.flush() after print statemtents

# initialize parser for command-line inputs
parser = argparse.ArgumentParser(description="multi-user chat server")
parser.add_argument("-join", dest="join", default=True, required=True, action="store_true", help="join server")
parser.add_argument("-host", dest="host", type=str, default=None, required=True, help="server ip address")
parser.add_argument("-port", dest="port", type=int, default=None, required=True, help="server port number")
parser.add_argument("-username", dest="username", type=str, default=None, required=True, help="client user name")
parser.add_argument("-passcode", dest="passcode", type=str, default=None, required=True, help="required passcode for joining the chat room")

args = parser.parse_args()

server_address = args.host
server_port = args.port
passcode = args.passcode
username = args.username


# create client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_address, server_port))

def receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "CONNECTED":
                # send passcode after connection is established
                client.send(passcode.encode("utf-8"))
            elif message == "AUTHORIZED":
                # send username after authorization granted (passcode validated)
                client.send(username.encode("utf-8"))
            elif message == "AUTH_FAIL":
                # authorization failed
                print("Invalid Passcode")
                client.close()
            elif message == "USER_INVALID":
                # username failed (invalid)
                print("Invalid Username")
                client.close()
            else:
                # message = "username: <sentence>"
                print(message)
        except:
            print("Error")
            client.close()
            break

def send_msg():
    while True:
        input_msg = input("")
        if input_msg == ":Exit":
            client.close()
            break

        message = f"{username}: {input_msg}"
        client.send(message.encode("utf-8"))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

send_msg_thread = threading.Thread(target=send_msg)
send_msg_thread.start()

#if __name__ == "__main__":
#	pass