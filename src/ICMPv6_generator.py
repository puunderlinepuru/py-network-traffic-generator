from scapy.all import *
from scapy.layers.inet6 import *

address = "fd00:1::2"


# ICMPv6 Echo Request (ping6)
ping_pkt = IPv6(dst=address) / ICMPv6EchoRequest(id=0x1234, seq=1, data=b"Hello IPv6")

resp = sr1(ping_pkt)

if resp:
    print("Received ICMP reply from", address)
else:
    print("No response received.")

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