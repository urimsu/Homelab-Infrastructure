# WireGuard tunnel works but LAN is unreachable

## Problem

A WireGuard peer shows a handshake, but a host behind the remote VPN gateway cannot be reached.

## Symptoms

The peer itself may respond while addresses on the LAN do not. This project encountered the distinction between tunnel establishment and routed connectivity; a single confirmed historical root cause is not asserted here.

## Architecture / Context

VPS ↔ WireGuard ↔ Raspberry Pi gateway ↔ anonymized home LAN (`192.168.X.0/24`).

## Hypotheses

Missing route or incorrect `AllowedIPs`; IPv4 forwarding disabled; FORWARD chain drops; destination host firewall; missing return route; NAT needed for the chosen topology; wrong interface or overlapping subnet.

## Investigation

Check the handshake and peer transfer counters. Inspect addresses and routes on both peers and the gateway. Test peer tunnel address, then LAN gateway, then destination service. Check forwarding and firewall counters while generating traffic.

## Commands Used

```bash
wg
ip addr
ip route
ping <VPN_PEER_IP>
ping <LAN_HOST_IP>
sysctl net.ipv4.ip_forward
iptables -L -n -v
iptables -t nat -L -n -v
```

## Root Cause

Not recorded as one universal cause. A successful handshake alone does not establish the LAN route.

## Solution

For the actual topology, align peer routes, enable forwarding where routing is required, allow only the intended interface pair, and provide a return route or deliberate NAT. Do not apply a broad forwarding rule without validating scope.

## Verification

Repeat a connection test at each hop and confirm firewall counters and return traffic. Test the actual protocol/port; ICMP may be filtered.

## Security Considerations

Limit `AllowedIPs` and forwarding rules to necessary networks. Avoid broad access from a public VPS peer into the entire LAN where a narrower path is possible.

## What I Learned

A WireGuard handshake proves that peers can communicate; it does not prove routed networks behind those peers are reachable.
