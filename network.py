import sys
import time
import socket
import threading

from random import randint

BYTE_SIZE = 1024
HOST = "0.0.0.0"
PORT = 6669
PEER_BYTE_DIFFERENTIATOR = b"\x11"
RAND_TIME_START = 1
RAND_TIME_END = 2
REQUEST_STRING = "req"


class Server:
    def __init__(self, msg):
        try:
            self.msg = msg
            self.connections = []
            self.peers = []

            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((HOST, PORT))
            self.s.listen(1)

            print("-" * 12 + "Server Running" + "-" * 21)

            self.run()
        except Exception as e:
            sys.exit()

    def handler(self, connection, a):

        try:
            while True:
                data = connection.recv(BYTE_SIZE)
                print("recieved", data.decode("utf-8"))
                for connection in self.connections:
                    if data and data.decode("utf-8")[0].lower() == "q":
                        self.disconnect(connection, a)
                        return
                    elif data and data.decode("utf-8") == REQUEST_STRING:
                        print("-" * 21 + " UPLOADING " + "-" * 21)
                        connection.send(self.msg)
        except Exception as e:
            sys.exit()

    def disconnect(self, connection, a):
        self.connections.remove(connection)
        self.peers.remove(a)
        connection.close()
        self.send_peers()
        print(f"{a}, disconnected")
        print("-" * 50)

    def run(self):
        while True:
            connection, a = self.s.accept()
            self.peers.append(a)
            print(f"peers list: {self.peers}")
            self.send_peers()
            c_thread = threading.Thread(target=self.handler, args=(connection, a))
            c_thread.daemon = True
            c_thread.start()
            self.connections.append(connection)
            print(f"{a}, connected")
            print("-" * 50)

    def send_peers(self):
        peer_list = ""
        for peer in self.peers:
            peer_list = peer_list + str(peer[0]) + ","

        for connection in self.connections:
            # data = PEER_BYTE_DIFFERENTIATOR + bytes(peer_list, "utf-8")
            connection.send(PEER_BYTE_DIFFERENTIATOR + bytes(peer_list, "utf-8"))


class Client:
    def __init__(self, addr):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.connect((addr, PORT))

        i_thread = threading.Thread(target=self.send_message)
        i_thread.daemon = True
        i_thread.start()

        while True:
            r_thread = threading.Thread(target=self.recieve_message)
            r_thread.start()
            r_thread.join()

            data = self.recieve_message()

            if not data:
                print("-" * 21 + " Server failed " + "-" * 21)
                break

            elif data[0:1] == b"\x11":
                print("updating peers")
                self.update_peers(data[1:])

    def recieve_message(self):
        try:
            print("client recieving")
            data = self.s.recv(BYTE_SIZE)
            print(data.decode("utf-8"))
            return data
        except KeyboardInterrupt:
            self.send_disconnect_signal()

    def update_peers(self, peers):
        p2p.peers = str(peers, "utf-8").split(",")[:-1]

    def send_message(self):
        try:
            self.s.send(REQUEST_STRING.encode("utf-8"))

        except KeyboardInterrupt as e:
            self.send_disconnect_signal()
            return

    def send_disconnect_signal(self):
        print("Disconnected from server")
        self.s.send("q".encode("utf-8"))
        sys.exit()


class p2p:
    peers = ["104.131.181.211"]


def main():
    msg = "test msg"
    while True:
        try:
            print("-" * 21 + "Trying to connect" + "-" * 21)
            time.sleep(randint(RAND_TIME_START, RAND_TIME_END))
            for peer in p2p.peers:
                try:
                    client = Client(peer)
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    pass

            # become the server
            try:
                server = Server(msg)
            except KeyboardInterrupt:
                sys.exit()
            except:
                pass

        except KeyboardInterrupt as e:
            sys.exit(0)


if __name__ == "__main__":
    main()
