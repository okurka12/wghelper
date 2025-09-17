import os
from subprocess import check_output
import ipaddress

DEFAULT_CONF = "example.conf"

def ipv4_to_number(ipv4: str) -> int:
    parts = [int(part) for part in ipv4.split(".")]

    if any(part > 255 for part in parts):
        raise ValueError(f"invalid IPv4 address: {ipv4}")

    return sum((
        parts[0] << 24,
        parts[1] << 16,
        parts[2] << 8,
        parts[3]
    ))


def ipv6_to_number(ipv6: str) -> int:
    parts = ipv6.split(":")

    # edge case: "::"
    if all(part == "" for part in parts):
        return 0

    tmp = []
    filled = False
    for part in parts:

        # fill zeroes
        if part == "" and not filled:
            tmp.extend([0 for _ in range(8 - len(parts) + 1)])
            filled = True

            if len(tmp) == 8:
                break

        elif part == "" and filled:
            tmp.append(0)

        else:
            part_int = int(part, 16)
            if part_int > 0xffff:
                raise ValueError(f"invalid IPv6 address: {ipv6}")
            tmp.append(part_int)

    parts = tmp

    assert len(parts) == 8

    return sum((
        parts[0] << 112,
        parts[1] << 96,
        parts[2] << 80,
        parts[3] << 64,
        parts[4] << 48,
        parts[5] << 32,
        parts[6] << 16,
        parts[7]
    ))


class Peer:
    def __init__(self, allowedips):
        """
        input examples:
        AllowedIPs = 10.0.0.2/32
        AllowedIPs = 10.0.0.2/32, fd00::2/128
        Address = 10.0.0.1/24, fd00::1/64
        """
        ips = allowedips.split("=")[1].strip()

        if len(ips.split(",")) == 1:
            self.ipv4 = ips.strip().split("/")[0]
            self.ipv6 = None
        elif len(ips.split(",")) == 2:
            self.ipv4 = ips.split(",")[0].strip().split("/")[0].strip()
            self.ipv6 = ips.split(",")[1].strip().split("/")[0].strip()
        else:
            raise RuntimeError(f"I cant parse this: {allowedips}")

    def __repr__(self):
        return f"Peer: {self.ipv4} {self.ipv6}"


print(ipv4_to_number("194.182.84.172"))
print(ipv6_to_number("fe80::f816:3eff:fe8a:3430"))
print(ipv6_to_number("fe80::"))
print(ipv6_to_number("::"))
print(ipv6_to_number("::ff"))

print(Peer("AllowedIPs = 10.0.0.2/32"))
print(Peer("AllowedIPs = 10.0.0.2/32, fd00::2/128"))
print(Peer("Address = 10.0.0.1/24, fd00::1/64"))
