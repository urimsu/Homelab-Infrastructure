# Security architecture

This is a personal homelab with evolving components. The security model focuses on reducing reachable services and limiting the effect of mistakes; it does not claim a formal zero-trust program or production assurance.

## Public and private surfaces

Selected application endpoints may be available through HTTPS on the VPS/reverse proxy. Administrative services—including Proxmox, SSH, Prometheus, Grafana administration, and the Nginx Proxy Manager control plane—are intended for the LAN or WireGuard path. Confirm exposure from the host, firewall, router, VPS, DNS, and authorized external vantage points.

## Operating principles

- Minimize public listeners; allow only reviewed application paths.
- Use WireGuard for remote administration and restrict peer routes.
- Apply default-deny firewall policy where practical, then allow required traffic explicitly.
- Validate IPv4 and IPv6 independently, including AAAA records and listening sockets.
- Prefer SSH keys for machine access and narrow command-specific sudo rules.
- Keep secrets out of Git; rotate a secret immediately if it is exposed.
- Patch supported operating systems and plan upgrades before EOL.
- Monitor both host metrics and service availability.
- Avoid exposing internal hostnames, addresses, query logs, or screenshots with identifying details.

## Firewall examples

The [example rules](../configs/firewall/example-rules.sh) are illustrative and require adaptation. Applying firewall changes remotely can lock out the operator. Preserve a recovery path and verify rule order, forwarding, established connections, and both protocol families.
