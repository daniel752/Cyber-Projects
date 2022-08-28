#This code was written for academic purposes only and never used with maliciuos intentions.
#I'm not responsible for any users actions with this code.


import binascii
import pickle
import socket


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


def calculate_missing_packet(missIndex,e,packets):
    # tempE = int(''.join(format(x,'b') for x in e))
    tempE = e
    for i in range(0,len(packets)-1,1):
        if packets[i].payload.packetIndex != missIndex:
            # print('Packet Data: ' + str(packets[i].data))
            # print('E: ' + tempE)
            tempE = ''.join(chr(ord(c1) ^ ord(c2)) for c1,c2 in zip(tempE,packets[i].data.decode()))

    print("Recovered missing packet's data: " + str(tempE))
    # print("Recovered missing packet's data: " + str(binary_to_ascii(str(tempE)).decode('utf-8','replace')))
    return UDPPacket(tempE,missIndex)


if __name__ == '__main__':
    localIP = "192.168.163.146"
    localPort = 12321
    buff_size = 1000
    msgFromServer = "Hello client"
    bytesToSend = str.encode(msgFromServer)
    counter = 1
    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Bind to address and ip
    UDPServerSocket.bind((localIP, localPort))
    print("UDP server up and listening")
    packetsIndexes = []
    packets = []
    flag = False

    # Listen for incoming datagrams
    while True:
        bytesAddressPair = UDPServerSocket.recvfrom(buff_size)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        packets.append(pickle.loads(message))
        packetsIndexes.append(pickle.loads(message).payload.packetIndex)
        if packetsIndexes[len(packetsIndexes) - 1] == pickle.loads(message).payload.d:
            break
        # checking each round if there's a packets missing
        # checking if there is a jump in indexes, like 1,2,3,5,...,d (packets with index 4 is missing)
        if len(packetsIndexes) > 1:
            if packetsIndexes[len(packetsIndexes) - 1] != packetsIndexes[len(packetsIndexes) - 2] + 1:
                # packet is missing
                missIndex = packetsIndexes[len(packetsIndexes) - 2] + 1
                print("Packet with index " + str(missIndex) + " didn't make it\n")
                flag = True

        # msg = UPDPacket(message,counter)
        clientMsg = "Message from Client:{}".format(pickle.loads(message).data)
        payload = "Payload:\nd = {}\nindex = {}\ne = {}\n".format(pickle.loads(message).payload.d,
                                                              pickle.loads(message).payload.packetIndex,
                                                              pickle.loads(message).payload.e)
        # clientIP = "Client IP Address:{}".format(address)
        print(clientMsg)
        print(payload)
        # print(counter)
        # counter += 1
        # Sending a reply to client
        UDPServerSocket.sendto(message, address)

    if flag:
        missMsg = calculate_missing_packet(missIndex,pickle.loads(message).payload.e,packets)