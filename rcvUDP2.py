import socket
import threading
import time
import datetime

UDP_IP = ""
UDP_PORT = 54540

cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
cs.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#we send it thrice to take care of possible packet loss
cs.sendto('This is a test', ('10.255.255.255', 54540))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((UDP_IP, UDP_PORT))

def client():
    # we also send our IP back to the client 
    # hardcoding our ip here, doesn't look like it's possible to discover our
    # IP in python when you're in an Ad-Hoc network
    ds = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ds.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        ds.sendto('Heres my IP back buddy', ('10.255.255.255', 54540))
        time.sleep(10)


threading.Thread(target=client).start()
network = list()
while True:
    data, addr = sock.recvfrom(20)
    # print addr
    # we add the ip to the list of IPs in the network
    new_nw = []
    for comb in network:
        if (datetime.datetime.now() - comb[1]).total_seconds() <= 30:
            new_nw.append(comb)

    network = new_nw
    for comb in network:
        if comb[0] == addr[0]:
            network.remove(comb)
            break
    network.append([addr[0], datetime.datetime.now()])
    print "#"
    for ip in network:
        print ip[0]

