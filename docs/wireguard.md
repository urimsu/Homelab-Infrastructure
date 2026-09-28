# WireGuard

WireGuard provides an encrypted path between the Linux VPS and the home side, with the Raspberry Pi used as a gateway in the design. It supports two different needs: selected reverse-proxy traffic toward an application and remote administrator access toward private management services.

## Routing model

`AllowedIPs` participates in peer selection and route configuration. It must describe the addresses that should use a peer without accidentally claiming unrelated networks. For routed access to a LAN behind a peer, the path also needs:

1. A route to the destination LAN on the sending side.
2. IPv4 forwarding enabled on the gateway when routing IPv4.
3. Forwarding firewall rules between the WireGuard and LAN interfaces.
4. A return route from the LAN, or a deliberately chosen NAT design.
5. Host-level firewall permission at the destination.

The tunnel may report a recent handshake while none of these routed conditions are satisfied. A handshake proves peer reachability, not reachability of networks behind a peer.

## Diagnostics

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

Interpret counters and routes alongside tests from each hop. A ping failure alone is inconclusive because ICMP may be filtered; test the actual service port too.

## Configuration safety

See [sanitized server example](../configs/wireguard/server.conf.example) and [client example](../configs/wireguard/client.conf.example). They use documentation ranges and invalid placeholder keys. Never commit a real private key. Restrict peer routes to the networks and services that need access, and keep management endpoints VPN-only.
