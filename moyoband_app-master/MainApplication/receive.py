import socket
import select
import os
import pandas as pd

HEADER_SIZE = 10
HOST_NAME = socket.gethostname()  # hostname of the machine where the Python interpreter is currently executing
PORT = 5005
BACKLOG = 5  # the number of unaccepted connections that the system will allow before refusing new connections
ENCODE_STAND = "utf-8"

MAIN_DIR_PATH = os.path.split(os.getcwd())[0]
FAKE_DATA_DIR = "fake_data_generator"
FAKE_DATA_FILE = "fake_data.txt"
FAKE_DATA_PATH = os.path.join(MAIN_DIR_PATH, FAKE_DATA_DIR, FAKE_DATA_FILE)


def receive_msg(client_socket):
    try:
        msg_header = client_socket.recv(HEADER_SIZE)
        if not len(msg_header):
            return False

        msg_length = int(msg_header.decode(ENCODE_STAND).strip())
        return {"header": msg_header, 'data': client_socket.recv(msg_length)}
    except:
        return False


def update_file(msg):
    """Updates fake_data.txt based on a msg
    msg should have a format of 'bed_id,patient_parameter,value"""

    data = msg.split(",")
    if len(data) != 3:
        print("Wrong format")
        return
    bed_id = data[0]
    patient_parameter = data[1]
    value = data[2]

    # not very efficient possible problems caused by value being a string
    df = pd.read_csv(FAKE_DATA_PATH)
    df.loc[df["bed_id"] == int(bed_id), patient_parameter] = value
    df.to_csv(FAKE_DATA_PATH, index=False)
    print("HI")


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST_NAME, PORT))
    server_socket.listen(BACKLOG)

    sockets_list = [server_socket]

    clients = {}

    print("HOST_NAME:", HOST_NAME)
    print("PORT:", PORT)
    print("Receiving messages...")

    while True:
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()

                user = receive_msg(client_socket)

                if user is False:
                    continue

                sockets_list.append(client_socket)
                clients[client_socket] = user

                print(
                    f"Accepted new connection from {client_address[0]}:{client_address[1]} "
                    f"username:{user['data'].decode(ENCODE_STAND)}")
            else:
                msg = receive_msg(notified_socket)
                if msg is False:
                    print(f"Closed connection from {clients[notified_socket]['data'].decode(ENCODE_STAND)}")
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]
                    continue

                user = clients[notified_socket]
                string_msg = msg['data'].decode(ENCODE_STAND)
                print(f"Received msg from {user['data'].decode(ENCODE_STAND)}: {string_msg}")

                update_file(string_msg)

                for client_socket in clients:
                    if client_socket != notified_socket:
                        client_socket.send(user["header"] + user["data"] + msg["header"] + msg["data"])

        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            del clients[notified_socket]


if __name__ == "__main__":
    main()
