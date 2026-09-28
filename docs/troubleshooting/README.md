# Troubleshooting index

These notes document diagnostic methods and known project context. Where the exact historical root cause is not established, the article describes hypotheses and verification steps without inventing a resolution.

- [WireGuard handshake works but LAN is unreachable](wireguard-routing.md)
- [Reverse proxy returns 502](reverse-proxy-502.md)
- [Service works locally but not remotely](service-local-only.md)
- [IPv4 blocked while IPv6 remains reachable](ipv6-exposure.md)
- [Raspberry Pi OS repository errors](raspberry-pi-repositories.md)
- [Discord bot dependency constraints](discord-bot.md)
- [Proxmox not reachable remotely](proxmox-remote-access.md)
- [DNS and reverse proxy mismatch](dns-proxy-mismatch.md)
- [Backend HTTP/HTTPS mismatch](backend-protocol.md)
- [Firewall rule too broad](firewall.md)
- [Monitoring endpoint unreachable](monitoring.md)
- [Wake-on-LAN troubleshooting](wake-on-lan.md)

## Method

Start from the service and move outward: local process, listening socket, host firewall, route, VPN, proxy, DNS, and external reachability. Change one variable at a time and capture the before/after result.
