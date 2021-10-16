import socket
import errno
import sys
from MainApplication.receive import HEADER_SIZE, PORT, ENCODE_STAND

HOST_NAME = "raspberrypi4"  # HOST_NAME needs to be the same as the name of the machine that is running receive.py


def main():
    my_username = input("Username: ")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST_NAME, PORT))
    client_socket.setblocking(False)

    username = my_username.encode(ENCODE_STAND)
    username_header = f"{len(username):<{HEADER_SIZE}}".encode(ENCODE_STAND)
    client_socket.send(username_header + username)

    while True:
        msg = input(f"{my_username} > ")
        if msg:
            msg = msg.encode(ENCODE_STAND)
            msg_header = f"{len(msg) :< {HEADER_SIZE}}".encode(ENCODE_STAND)
            client_socket.send(msg_header + msg)

        try:
            while True:
                # receive things
                username_header = client_socket.recv(HEADER_SIZE)
                if not len(username_header):
                    print("connection closed by the server")
                    sys.exit()
                username_length = int(username_header.decode(ENCODE_STAND).strip())  # maybe wrong
                username = client_socket.recv(username_length).decode(ENCODE_STAND)

                msg_header = client_socket.recv(HEADER_SIZE)
                msg_length = int(msg_header.decode(ENCODE_STAND).strip())
                msg = client_socket.recv(msg_length).decode(ENCODE_STAND)

                print(f"{username} > {msg}")

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print("reading error", str(e))
                sys.exit()
            continue
        except Exception as e:
            print("General error", str(e))


if __name__ == "__main__":
    main()
