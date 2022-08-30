#Any actions and or activities related to the code provided is solely your responsibility.
#The misuse of the information in this website can result in criminal charges brought against the persons in question.
#The authors will not be held responsible in the event any criminal charges be brought against any individuals misusing
#the information in this tool to break the law.


import os
import pickle
import socket

from scapy.layers.inet import IP, UDP

from UDPClient import UDPPacket,PacketPayload
from scapy.sendrecv import srp, sniff
from scapy.layers.l2 import ARP, Ether,srp
from scapy.sendrecv import send
import time
import argparse
import sys
import scapy
from scapy import plist
from scapy.plist import PacketList
from pickle import *


# function that gets a packet in bytes
# convert that packet of bytes to normal text
# display packet's data
def check_packet(packetBytes):
    packet = pickle.loads(packetBytes['Raw'].load)
    udpPacket = "Packet Data:\n{}" \
                "\nSequence No: {}" \
                "\nPayload:\nd = {}" \
                "\nindex = {}\ne = {}\n".format(packet.data,
                                                packet.seq_num,
                                                packet.payload.d,
                                                packet.payload.packetIndex,
                                                packet.payload.e)
    print(udpPacket)


print("Ready to sniff")
while True:
    try:
        # sniffing for packets on specified interface ('iface')
        # filtering to show only UDP protocol with specified destination port,destination host and source host
        # after each sniff the lambda function will be called
        sniff(iface="VMware Virtual Ethernet Adapter for VMnet8",
              filter="udp and (dst port 12321) and (dst host 192.168.163.146 and src host 192.168.163.145)",
              prn=lambda x: check_packet(x))

    # in case user want's to stop the program using ctrl+c
    except KeyboardInterrupt:
        print("\nSniffing stopped")
        sys.exit(0)
