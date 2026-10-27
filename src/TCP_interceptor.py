from scapy.all import *
from scapy.layers.inet import IP, TCP

import time

# ── Configuration ──────────────────────────────────────────────
LAN_IP    = "192.168.1.100"   # source address on LAN
SRV_IP    = "203.0.113.10"    # server address
PORT      = 80
# ───────────────────────────────────────────────────────────────

# seq/ack adjustment table: (src_ip, dst_ip, is_syn) -> (seq_delta, ack_delta)
# is_syn: 1 for SYN, 0 for ACK/established
_deltas = {}

# ICN (new initial sequence number) for the first SYN
NEW_ICN = 1000


def _get_delta(pkt, is_syn):
    key = (pkt[IP].src, pkt[IP].dst, is_syn)
    return _deltas.get(key, (0, 0))


def _set_delta(pkt, is_syn, seq_delta, ack_delta):
    key = (pkt[IP].src, pkt[IP].dst, is_syn)
    _deltas[key] = (seq_delta, ack_delta)


def _forward(pkt, src_ip, dst_ip, new_src, new_dst):
    p = IP(src=new_src, dst=new_dst, proto=6) / pkt[TCP]
    p[TCP].seq = pkt[TCP].seq + pkt[TCP].window - pkt[TCP].window  # keep
    # recompute
    # original seq already set; just send
    p[TCP].chksum = None
    send(p, iface="eth0")


def handle(pkt):
    ip  = pkt[IP]
    tcp = pkt[TCP]
    is_syn = (tcp.flags & 0x02) != 0
    seq_delta, ack_delta = _get_delta(pkt, is_syn)

    # ── first SYN from LAN ──
    if is_syn and ip.src == LAN_IP:
        # compute new ICN
        new_icn = NEW_ICN
        old_icn = tcp.seq
        _set_delta(pkt, 1, new_icn - old_icn, 0)
        # outgoing
        _set_delta(pkt, 0, 0, new_icn - old_icn)
        # build forwarded packet
        f = IP(src=LAN_IP, dst=SRV_IP, proto=6) / \
            TCP(seq=new_icn, ack=tcp.ack,
                flags=tcp.flags, options=tcp.options)
        f[TCP].chksum = None
        send(f, iface="eth0")
        return

    # ── subsequent: LAN → server ──
    if ip.src == LAN_IP:
        _set_delta(pkt, 0, 0, tcp.seq + seq_delta - tcp.seq + ack_delta - tcp.ack + tcp.ack - tcp.ack)
        # simpler:
        # new seq = seq + (new_icn - old_icn) = seq + seq_delta (syn=0 row)
        # new ack = ack + ack_delta
        f = IP(src=LAN_IP, dst=SRV_IP, proto=6) / \
            TCP(seq=tcp.seq + seq_delta, ack=tcp.ack + ack_delta,
                flags=tcp.flags, options=tcp.options)
        f[TCP].chksum = None
        send(f, iface="eth0")
        # save
        _set_delta(pkt, 0, seq_delta, ack_delta)
        return

    # ── server → LAN ──
    # (handled by the 0-row stored above)
    # new seq = seq + seq_delta(0)
    # new ack = ack + ack_delta(0)
    f = IP(src=SRV_IP, dst=LAN_IP, proto=6) / \
        TCP(seq=tcp.seq + seq_delta, ack=tcp.ack + ack_delta,
            flags=tcp.flags, options=tcp.options)
    f[TCP].chksum = None
    send(f, iface="eth0")


def main():
    print(f"Listening on {LAN_IP}:{PORT}  →  {SRV_IP}:{PORT}")
    while True:
        sniff(iface="eth0",
              filter=f"src host {LAN_IP} and dst port {PORT} or "
                     f"src host {SRV_IP} and dst port {PORT}",
              prn=handle)


if __name__ == "__main__":
    main()
