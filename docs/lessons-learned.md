# Lessons learned

1. **A WireGuard handshake does not prove routing works.** Routes, forwarding, firewall rules, and return paths also matter.
2. **A reverse proxy adds another network layer.** Debug the backend path separately from proxy host and TLS settings.
3. **Test the backend before DNS.** This avoids changing names when the service is offline or unreachable.
4. **IPv6 needs its own firewall review.** IPv4 restrictions can leave another path available.
5. **Compare listening ports with intended exposure.** A running service may bind to an unexpected interface.
6. **Keep management interfaces private.** Remote access through VPN is easier to audit than public admin listeners.
7. **Automation should have least privilege.** A bot should not gain a general shell or unrestricted sudo.
8. **EOL operating systems become operational and security liabilities.** Archived repositories are not a durable patch strategy.
9. **Metrics and uptime checks answer different questions.** Use both when both resource health and availability matter.
10. **Documentation becomes more valuable as boundaries multiply.** Record actual state and uncertainty.
11. **Power use matters for always-on hardware.** Measure average draw and balance availability with runtime.
12. **Infrastructure work is iterative.** Design, deploy, break, investigate, fix, and document.

## Design decisions and tradeoffs

| Decision | Reason | Tradeoff |
|---|---|---|
| Proxmox on existing server hardware | Learn virtualization and run separated workloads | Older hardware, power draw, and storage/controller complexity |
| VPS plus WireGuard | Stable public entry and encrypted home path | Additional host, routing, patching, and tunnel dependencies |
| Avoid direct Proxmox exposure | Reduce risk to the management plane | Administration depends on VPN availability |
| Reverse proxy selected apps | Present a small HTTPS surface | More DNS, TLS, and backend routing to troubleshoot |
| Raspberry Pi utility node | Low-power gateway and automation host | Small resource budget and gateway dependency |
| Pi-hole | DNS filtering and local naming | Cannot reliably filter same-domain ads; client DNS may bypass it |
| Prometheus/Grafana plus Uptime Kuma | Resource history and availability checks | More services to secure and maintain |
| Wake-on-LAN | Reduce always-on runtime | Boot delay and hardware/network dependencies |
| Dynamic CPU scaling | Reduce frequency under lighter load | Must measure workload and actual power effect |

Choices evolved through experimentation. The table records rationale and tradeoffs, not claims that every design choice was permanent or optimal.
