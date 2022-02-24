import socket
import threading
import sys 
import argparse
import datetime

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

shortcut = {
    ":)" : "[feeling happy]",
    ":(" : "[feeling sad]",
    ":mytime" :str(datetime.datetime.now().time()), 
    ":+1hr" :str((datetime.datetime.now() + datetime.timedelta(hours=1)).time()),
}

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
                print("Incorrect passcode")
                sys.stdout.flush()
                client.close()
            elif message == "USER_INVALID":
                # username failed (invalid)
                print("Invalid username")
                sys.stdout.flush()
                client.close()
            else:
                # message = "username: <sentence>"
                print(message)
                sys.stdout.flush()
        except:
            print("Error")
            sys.stdout.flush()
            client.close()
            sys.exit()
            break

def send_msg():
    while True:
        try:
            input_msg = input("")

            if input_msg == ":Exit":
                client.send("CONNECTION-CLOSE".encode("utf-8"))
                client.shutdown(1)
                client.close()
                sys.exit()
                break

            if input_msg in shortcut:
                input_msg = shortcut[input_msg]

            message = f"{username}: {input_msg}"
            client.send(message.encode("utf-8"))
        except:
            client.close()
            sys.exit()
            break


receive_thread = threading.Thread(target=receive)
receive_thread.start()

send_msg_thread = threading.Thread(target=send_msg)
send_msg_thread.start()

#if __name__ == "__main__":
#	pass