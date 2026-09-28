# Networking

The network design evolved from a home LAN to include a VPS, WireGuard routing, selected public application paths, and VPN-only administration. The home network is anonymized as `192.168.X.0/24`; replace placeholders only in local private notes.

## Packet path as a troubleshooting tool

For a remote request, reason through each boundary:

```text
client → DNS → public listener → reverse proxy → VPN route
→ home gateway → LAN route/firewall → backend listener
```

An error at one step is not evidence that the next step is faulty. Check a service from its own host first, then from the proxy, then through the tunnel, then from an authorized external client.

## Routes, forwarding, and NAT

Routing decides where a packet should go. IPv4 forwarding allows a Linux host to route between interfaces. Firewall forwarding policy decides whether it may pass. NAT/MASQUERADE can make return traffic work when the downstream network has no route back, but it changes source-address visibility and should not be added without understanding the return path.

Useful inspection commands:

```bash
ip addr
ip route
sysctl net.ipv4.ip_forward
ss -tulpn
iptables -L -n -v
iptables -t nat -L -n -v
```

## DNS and address families

Check A and AAAA records separately. A service may be reachable over IPv6 even when IPv4 is blocked, or the reverse. Check the address the client resolved and the address on which the service is listening. DNS does not establish that a backend route is healthy.

## Exposure review

Maintain an expected-exposure list and compare it with listening sockets, host firewalls, router/VPS policy, and authorized external observations. Repeat checks for IPv4 and IPv6. Ports such as 8006 (Proxmox), 9090 (Prometheus), and 9100 (Node Exporter) are examples of service defaults, not statements of actual exposure.

| Service | LAN | VPN | Public | Design intent |
|---|---:|---:|---:|---|
| SSH | yes | yes | no | Administration |
| Proxmox UI | yes | yes | no | Management |
| Prometheus | yes | yes | no | Monitoring backend |
| Grafana administration | yes | yes | no | Private dashboards |
| Nginx Proxy Manager administration | yes | yes | no | Proxy control plane |
| Selected HTTPS proxy host | n/a | n/a | yes | Deliberately published application |

This is a design example, not an inventory of active listeners. Compare expected exposure with local sockets and authorized external checks. For assets you own or have explicit permission to assess, a limited TCP scan can help validate the public edge:

```bash
nmap -sT <OWN_SERVER>
nmap -sV <OWN_SERVER>
```

Service/version detection sends additional probes. Define scope and rate appropriately, and check IPv6 separately when the target has IPv6 connectivity.
