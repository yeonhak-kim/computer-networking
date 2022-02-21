import socket
import threading
import sys 
import argparse

#TODO: Implement all code for your server here

# Use sys.stdout.flush() after print statemtents


def main(argv):
	# initialize parser for command-line inputs
	parser = argparse.ArgumentParser(description="multi-user chat server")
	parser.add_argument("-start", dest="start", default=True, required=True, action="store_true", help="start server")
	parser.add_argument("-port", dest="port", default=None, required=True, help="server port number")
	parser.add_argument("-passcode", dest="passcode", default=None, required=True, help="required passcode for joining the chat room")
	args = parser.parse_args()

	print(args.start, args.port, args.passcode)


if __name__ == "__main__":
	main(sys.argv[1:])
