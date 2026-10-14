from scapy.layers.inet6 import ICMPv6ND_NA, ICMPv6ND_NS, ICMPv6ND_RA, ICMPv6NDOptDstLLAddr, ICMPv6NDOptPrefixInfo, ICMPv6NDOptRDNSS, ICMPv6NDOptSrcLLAddr, IPv6, ICMPv6EchoRequest
from scapy.sendrecv import sr1
from ICMPv4_generator import send_icmp

"""
FIELDS

Flow Label - HIGH
Extension header padding/Options = HIGH

Traffic Class = MEDIUM
Fragment Header = MEDIUM
Address fields =  LOW to MEDIUM
"""


address = "fd00:1::2"

text = "text"
encoded_text = text.encode('utf-8')
print(encoded_text[0])

# ICMPv6 Echo Request (ping6)
# ping_pkt = IPv6(dst=address) / ICMPv6EchoRequest(id=0x1234, seq=1, data=b"Hello IPv6")

def send_icmpv6(
        ipv6_version = 6,
        traffic_class = 0,
        flow_label = 0,
        payload_length = None,
        next_header = 58,
        hop_limit = 255,
        source=None,
        destination=address
):

    ipv6_header = IPv6(
        version=ipv6_version, 
        tc=traffic_class, 
        fl=flow_label, 
        plen=payload_length, 
        nh=next_header, 
        hlim=hop_limit, 
        src=source, 
        dst=destination
        )

    ping_pkt = ipv6_header / ICMPv6EchoRequest(id=0x1234, seq=1, data=b"Hello IPv6")

    resp = sr1(ping_pkt)

    if resp:
        print("Received ICMP reply from", address)
    else:
        print("No response received.")

def ICMPv6_generate_hlim(message):
    encoded_text = message.encode('utf-8')
    for byte in encoded_text:
        print(byte)
        send_icmp(src_ip="192.168.1.68", dest_ip="192.168.1.2", time_to_live=byte)
        send_icmpv6(hop_limit=byte)

ICMPv6_generate_hlim(text)

"""
# ICMPv6 Echo Reply
reply_pkt = IPv6(dst=address) / ICMPv6EchoReply(id=0x1234, seq=1)

# ICMPv6 Destination Unreachable
unreach = IPv6(dst=address) / ICMPv6DestUnreach(code=0)

# Neighbor Solicitation (NDP NS)
ns = IPv6(dst="ff02::1:ff00:1", hlim=255) / \
     ICMPv6ND_NS(tgt="2001:db8::1") / \
     ICMPv6NDOptSrcLLAddr(lladdr="de:ad:be:ef:00:01")

# Neighbor Advertisement (NDP NA)
na = IPv6(src="2001:db8::1", dst="ff02::1", hlim=255) / \
     ICMPv6ND_NA(tgt="2001:db8::1", R=0, S=0, O=1) / \
     ICMPv6NDOptDstLLAddr(lladdr="de:ad:be:ef:00:01")

# Router Advertisement
ra = IPv6(src="fe80::1", dst="ff02::1", hlim=255) / \
     ICMPv6ND_RA(chlim=64, M=0, O=0) / \
     ICMPv6NDOptPrefixInfo(
         prefixlen=64,
         L=1, A=1,
         validlifetime=86400,
         preferredlifetime=14400,
         prefix="2001:db8:1::"
     ) / \
     ICMPv6NDOptRDNSS(lifetime=300, dns=["2606:4700:4700::1111"])

# Send RA (requires root/CAP_NET_RAW)
# sendp(Ether(dst="33:33:00:00:00:01") / ra, iface="eth0", verbose=False)
"""