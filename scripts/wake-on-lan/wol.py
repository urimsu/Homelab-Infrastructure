#!/usr/bin/env python3
"""Send a Wake-on-LAN magic packet to an explicitly configured MAC."""

from __future__ import annotations

import os
import re
import socket
import sys


MAC_PATTERN = re.compile(r"^(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")


def main() -> int:
    mac = os.environ.get("WOL_MAC_ADDRESS", "AA:BB:CC:DD:EE:FF")
    broadcast = os.environ.get("WOL_BROADCAST", "192.0.2.255")
    try:
        port = int(os.environ.get("WOL_PORT", "9"))
    except ValueError:
        print("WOL_PORT must be an integer.", file=sys.stderr)
        return 2

    if not MAC_PATTERN.fullmatch(mac):
        print("WOL_MAC_ADDRESS must use the format AA:BB:CC:DD:EE:FF.", file=sys.stderr)
        return 2
    if not 1 <= port <= 65535:
        print("WOL_PORT must be between 1 and 65535.", file=sys.stderr)
        return 2
    if mac == "AA:BB:CC:DD:EE:FF":
        print("Set WOL_MAC_ADDRESS to the target NIC's MAC address first.", file=sys.stderr)
        return 2

    try:
        mac_bytes = bytes.fromhex(mac.replace(":", ""))
        packet = b"\xff" * 6 + mac_bytes * 16
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(packet, (broadcast, port))
    except (OSError, ValueError) as exc:
        print(f"Could not send Wake-on-LAN packet: {exc}", file=sys.stderr)
        return 1

    print(f"Sent Wake-on-LAN packet to configured target via {broadcast}:{port}.")
    print("Verify the host booted with a separate authorized health check.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
