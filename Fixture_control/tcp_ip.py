import time
import socket

class TCPClient:
    def __init__(self, server_address):
        self.server_address = server_address
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect(self.server_address)

    def disconnect(self):
        self.client_socket.close()

    def send_message(self, message):
        self.client_socket.connect(self.server_address)
        self.client_socket.settimeout(10)
        time.sleep(1)
        self.client_socket.sendall(message.encode())

    def receive_response(self):
        response = self.client_socket.recv(1024)
        return response.decode()

    def send_receive_data(self, message):
        self.client_socket.sendall(message.encode())
        time.sleep(1)
        response = self.client_socket.recv(1024)
        return response.decode()

    def close(self):
        self.client_socket.close()


if __name__ == '__main__':
    server_address = ('127.0.0.1', 22)
    client = TCPClient(server_address)
    # client.connect()
    # print(client)
    # time.sleep(2)
    # client.disconnect()
    # print('disconnect...')
    # client = TCPClient(server_address)
    # client.connect()
    # Open sequence
    # sequence = 'D:\\123.seq'
    # command = 'OPEN;%s \r\n'%(sequence) #'D:\\123.seq'
    client.client_socket.settimeout(5)
    message = '123'
    client.send_message(message)

    response = client.receive_response()
    print('接收到响应:', response)
    # time.sleep(10)
    # time.sleep(2)
    client = TCPClient(server_address)
    # client.connect()
    message = '456'
    client.send_message(message)

    response = client.receive_response()
    print('接收到响应:', response)

    # client.close()
