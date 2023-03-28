import socket
import struct


# def create_packet(id):
#     """Create a new echo request packet based on the given "id"."""
#     # Header is type (8), code (8), checksum (16), id (16), sequence (16)
#     header = struct.pack('bbHHh', 8, 0, 0, id, 1)
#     print(header)
#     packet = icmpPacket()
#     print(packet.computeChecksum(header, 64))
#     return header


def listOfWords(byteObject) -> list:
    return [byteObject[i:i + 2] for i in range(0, len(byteObject), 2)]


class icmpPacket:
    def __init__(self, icmpID, sequence):
        self.ICMP_PROTO_CODE = socket.getprotobyname('icmp')
        self.ICMP_ECHO = 8
        self.ID = icmpID
        self.sequence = sequence

    def create_packet(self):
        """Create a new echo request packet based on the given "id"."""
        # Header is type (8), code (8), checksum (16), id (16), sequence (16)
        # header = struct.pack('bbHHh', 8, 0, 0, id, 1)
        header = struct.pack('!bbHHh', self.ICMP_ECHO, 0, 0, self.ID, self.sequence)
        data = b'TEST'
        pktCksum = self.computeChecksum(header + data, 64)
        header = struct.pack('!bbHHh', self.ICMP_ECHO, 0, -pktCksum, self.ID, self.sequence)
        return header + data

    def send(self):
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, self.ICMP_PROTO_CODE)
        host = socket.gethostbyname('www.google.com')
        packet = self.create_packet()
        my_socket.sendto(packet, (host, 1))
        my_socket.close()

    # The checksum function is a python implementation
    # of in_cksum function from ping.c source code
    # Source: https://github.com/amitsaha/ping/blob/master/ping.c
    # All right reserved to the original author
    @staticmethod
    def computeChecksum(packet, packetLen):
        csum = 0
        listPacket = listOfWords(packet)

        for wordPkt in listPacket:
            csum = csum + int.from_bytes(wordPkt, "big")

        csum = (csum >> 16) + (csum & 0xffff)
        csum = csum + (csum >> 16)
        answer = ~csum

        return answer


if __name__ == '__main__':
    icmpkt = icmpPacket(1, 9)
    icmpkt.send()
