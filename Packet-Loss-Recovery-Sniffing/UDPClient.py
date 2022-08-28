#This code was written for academic purposes only and never used with maliciuos intentions.
#I'm not responsible for any users actions with this code.


import math
import pickle
import socket
import time
import sys
from random import randint
from sys import stdout
from time import sleep
from operator import xor
from scapy.layers.inet import *
from scapy.sendrecv import *


class UDPPacket:
    def __init__(self, data, seq_num, payload=None):
        if payload is None:
            payload = []
        self.data = data
        self.seq_num = seq_num
        self.payload = payload


class PacketPayload:
    def __init__(self,d,e,packetIndex):
        self.d = d
        self.e = e
        self.packetIndex = packetIndex


def make_d_packets(packets):
    temp = d
    i = 0
    # make 'd' (number of packets) packets from message
    while temp >= 0:
        packets.append(UDPPacket(msgFromClient[i:i + packetSize], seq_num))
        i += packetSize
        temp -= 1
    # for i in range(0,len(packets) - 1,1):
    #     if len(packets[i].data) != packetSize:
    #         newPackets = []
    #         print('Packet #' + str(i) + ' did not split well, so i will throw it away')
    #         badIndex = i
    #         for j in range(0,len(packets) - 1,1):
    #             if j != badIndex:
    #                 newPackets[j] = packets[i]
    #         return newPackets
    return packets


# calculate e: XOR between 'd' (number of packets) packets
def calculate_e(packets):
    # converting packets data (string/char) to int and then to binary while slicing the '0b' (2 first bits)
    # e equals the first packet
    e = packets[0].data.decode()
    # e = int(''.join(format(x,'b') for x in packets[0].data))
    # print(type(e))
    # e = packets[0].data
    # print(e)
    for i in range(1,len(packets) - 1):
        # if i == 1:
        #     e = ''.join(chr(ord(c1) ^ ord(c2)) for c1,c2 in zip(packets[i],packets[i+1]))
        # print(packets[i].data)
        # print(int(''.join(format(x,'b') for x in packets[i].data)))
        e = ''.join(chr(ord(c1) ^ ord(c2)) for c1,c2 in zip(e,packets[i].data.decode()))
        # print(str(i) + '.e = ' + e + '\n')
    return e


def base10to2(num):
    if int(num) <= 1:
        return num
    binaryValue = ''
    decimalRemainder = int(num)
    while decimalRemainder > 0:
        binaryValue = str(decimalRemainder % 2) + binaryValue
        decimalRemainder = math.floor(decimalRemainder // 2)
    return binaryValue


# filling all packets with payload
# random number d, e = packet[0] XOR packet[1] XOR ... packet[d], packet index i
def fill_packets_payload(packets):
    for i in range(len(packets)):
        packets[i].payload = PacketPayload(d,e,i)
    return packets


def send_packets(packets, serverAddressPort):
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    for i in range(len(packets)):
        if i == 4:
            print('Lost Packet\'s Data:' + str(packets[i].data) + '\n')
            continue
        sleep(3)
        packets[i].seq_num = i
        temp = pickle.dumps(packets[i])
        # print(temp)
        sock.sendto(temp,serverAddressPort)
        print(pickle.loads(sock.recv(buffer_length)).data)
        print()


if __name__ == '__main__':
    buffer_length = 1000
    counter = 1
    my_file = r"/home/daniel/Cyber/random_text.txt"
    f = open(my_file, "rb")
    # # Reading the buffer length in file_data
    # file_data =
    msgFromClient = f.read(buffer_length)
    bytesToSend = str.encode("msgFromClient")
    serverAddressPort = ("192.168.163.146", 12321)
    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # generate random number d
    d = randint(11, 35)
    #d = 10
    # packets size
    packets = []
    packetSize = int(buffer_length / d)
    seq_num = 0
    try:
	    packets = make_d_packets(packets)
	    e = calculate_e(packets)
	    packets = fill_packets_payload(packets)
	    send_packets(packets,serverAddressPort)
    except KeyboardInterrupt:
    	print('\nProgram stopped')
    	sys.exit(0)
    # Send to server using created UDP socket
    # while True:
    #     time.sleep(3)
    #     packet = UDPPacket(msgFromClient, counter)
    #     counter += 1
    #     if UDPClientSocket.sendto(packet.data, serverAddressPort):
    #         msgFromClient = f.read(buffer_length)
    #         print(counter)
    #
    #     msgFromServer = UDPClientSocket.recvfrom(buffer_length)
    #     msg = "Message from Server {}\n".format(msgFromServer[0])
    #     print(msg)
