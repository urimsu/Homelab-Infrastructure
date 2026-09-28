# Project evolution

The system grew by adding capabilities when a concrete need appeared. The sequence below captures the direction of that work; some components were experiments and were not necessarily active together.

```mermaid
flowchart TD
  A[Physical TX200 S7] --> B[Proxmox VE]
  B --> C[VMs and LXC]
  C --> D[Need for remote access]
  D --> E[Linux VPS]
  E --> F[WireGuard peer and tunnel]
  F --> G[Routing between VPS and home LAN]
  G --> H[Manual Nginx reverse proxy]
  H --> I[Nginx Proxy Manager exploration]
  G --> J[Raspberry Pi infrastructure node]
  J --> K[Pi-hole / DNS]
  C --> L[Prometheus and Grafana]
  C --> M[Uptime Kuma]
  J --> N[Wake-on-LAN and Discord automation]
  B --> O[Power and lifecycle investigation]
  O --> P[CPU governor / scheduled availability]
```

Each addition also created a new failure domain. A reverse proxy required a working backend route, correct protocol, and DNS. VPN access required more than a handshake: route selection, kernel forwarding, and firewall policy all had to agree. Monitoring then made resource use and availability easier to observe.

The chronology is a learning narrative, not a claim that every stage was a formal production deployment. Future improvements should be labeled as planned until verified.
