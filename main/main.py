import socket
import struct

class IcmpPacketSender:

    def __init__(self, target_ip, port=None, data=None, ttl=64, icmp_id=12345):
        self.target_ip = target_ip
        self.port = port
        self.data = data
        self.ttl = ttl
        self.icmp_id = icmp_id

    def send_icmp_packet(self):
        # Create raw socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

        # Set socket TTL
        # sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack("I", self.ttl))
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        # Set socket timeout
        sock.settimeout(2)

        ip_header = b'\x45\x00\x00\x54\x18\x0e\x40\x00\x40\x01\x24\x99\x7f\x00\x00\x01\x7f\x00\x00\x01'


        icmp_type = 8  # ICMP echo request
        icmp_code = 0
        icmp_checksum = 0
        icmp_sequence = 1

        # ICMP payload (data)
        if self.data:
            icmp_payload = self.data.encode()
        else:
            icmp_payload = b"test"

        # ICMP header
        icmp_header = struct.pack("!BBHHH", icmp_type, icmp_code, icmp_checksum, self.icmp_id, icmp_sequence)

        # Calculate checksum
        icmp_checksum = self.calculate_checksum(icmp_header + icmp_payload)

        # Update ICMP header with correct checksum
        icmp_header = struct.pack("!BBHHH", icmp_type, icmp_code, socket.htons(icmp_checksum), self.icmp_id, icmp_sequence)

        # Create ICMP packet
        icmp_packet = icmp_header + icmp_payload

        print("icmp_packet: \n", icmp_packet)

        packet = ip_header + icmp_packet

        print("packet: \n", packet)

        # Send packet
        if self.port:
            sock.sendto(packet, (self.target_ip, self.port))
        else:
            sock.sendto(packet, (self.target_ip, 0))

        print("ICMP packet sent successfully!")

    def calculate_checksum(self, data):
        checksum = 0

        # Handle odd-length data
        if len(data) % 2 != 0:
            data += b"\x00"

        # Calculate checksum
        for i in range(0, len(data), 2):
            checksum += (data[i] << 8) + data[i+1]

            checksum = (checksum >> 16) + (checksum & 0xffff)
            checksum += checksum >> 16

            print("checksum:", ~checksum)

            # return (~checksum) & 0xffff
            return 0xebdf

def main():
    target_ip = input("Enter target IP: ")
    port = int(input("Enter port (optional, press Enter to skip): ") or 0)
    data = input("Enter data (optional, press Enter to use default): ")
    ttl = int(input("Enter TTL (optional, press Enter to use default): ") or 64)
    icmp_id = int(input("Enter ICMP ID (optional, press Enter to use default): ") or 12345)

    icmp_packet_sender = IcmpPacketSender(target_ip, port, data, ttl, icmp_id)
    icmp_packet_sender.send_icmp_packet()

if __name__ == "__main__":
    main()