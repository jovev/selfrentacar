import socket
import binascii


HOSTS = "127.0.0.1"
PORTS = 3000


HOST = "192.168.1.113"
PORT = 3000 



dobar_format = bytearray.fromhex("02023030303030303030303030313030301C311C1C2B301C3934311C1C1C1C1C1C1C1C1C1C1C30301C1C1C1C1C1C1C1C1C0324").decode()

seSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
odooSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
seSock.connect(HOST, PORT)

try:
    # odooSock.bind((HOSTS, PORTS))
    seSock.sendto(dobar_format)

    while True:
        try:
            print("try prvi")
            # utp_data, address = odooSock.recvfrom(1024)
            # data = binascii.hexlify(utp_data).decode()
            # print(data)
        except:
            print("except drugi")

except:
    print("Ode na except prvi")