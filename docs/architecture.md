# Architecture

## Current design model

The homelab is documented as a set of roles that were introduced over time. The diagram is a conceptual view, not an uptime or deployment inventory.

```mermaid
flowchart TB
  subgraph Public[Public network]
    Internet((Internet))
    Client[Remote client]
  end
  subgraph Edge[Public edge]
    VPS["VPS<br/>Linux / HTTPS entry / WireGuard peer"]
    Proxy["Nginx or Nginx Proxy Manager<br/>selected application hosts"]
  end
  subgraph Tunnel[Encrypted private path]
    WG{{WireGuard tunnel}}
  end
  subgraph Home[Home network 192.168.X.0/24]
    PI["Raspberry Pi<br/>VPN routing / Pi-hole / automation"]
    PVE["Proxmox VE<br/>TX200 S7"]
    VM[VMs]
    LXC[LXC containers]
    Service[Selected application backend]
    Admin["Private management<br/>SSH / Proxmox / dashboards"]
    Metrics[Node Exporter → Prometheus → Grafana]
    Uptime[Uptime Kuma]
  end
  Internet -->|HTTPS to selected host| VPS
  VPS --> Proxy
  Proxy --> WG --> PI
  PI --> Service
  Client -->|VPN for administration| WG
  PI --> PVE --> VM --> Service
  PVE --> LXC --> Service
  WG --> Admin
  Service --> Metrics
  Service --> Uptime
```

## Trust boundaries

```mermaid
flowchart LR
  Internet((Internet)) -->|only selected HTTPS| Public[Public application edge]
  Public -->|WireGuard / routed backend| HomeApp[Selected home application]
  Internet -. no direct management path .-> Mgmt[Management plane]
  Admin[Authorized remote admin] -->|WireGuard| Mgmt
  Mgmt --> Proxmox[Proxmox / SSH]
  Mgmt --> Observability[Prometheus / Grafana / NPM admin]
```

The public edge and management plane have different purposes. The reverse proxy is an entry point for selected applications; it does not make administrative interfaces appropriate for public exposure. The actual firewall and route configuration must be checked on each host, including IPv6.

## Request flows

### Public application

```mermaid
sequenceDiagram
  participant U as Internet client
  participant V as VPS / HTTPS proxy
  participant W as WireGuard
  participant A as Selected backend
  U->>V: HTTPS request for configured host
  V->>W: Forward selected request over tunnel
  W->>A: Request backend over private route
  A-->>U: Response through proxy and tunnel
```

### Administration

```mermaid
sequenceDiagram
  participant R as Remote administrator
  participant W as WireGuard
  participant H as Home LAN
  participant P as Proxmox / private service
  R->>W: Establish authenticated VPN peer
  W->>H: Route only permitted management networks
  H->>P: Connect to management service
  P-->>R: Response over VPN
```

## Addressing and storage

Public documentation uses `192.168.X.0/24` for an anonymized home network and placeholders for host addresses. Where examples need a public IPv4 address, use RFC 5737 documentation ranges. Storage must be understood in layers: physical SAS disks connect to a hardware RAID controller, which can present logical volumes to Linux; Linux block devices are then used by Proxmox storage definitions and guest disks. The RAID level and exact storage layout have not been verified here.

## Implemented, explored, planned

Proxmox virtualization, remote access experiments, reverse proxying, DNS filtering, monitoring, Wake-on-LAN, and Discord/SSH automation are part of the project history. The exact deployment state changed over time. Do not infer that every component shown above is currently active or that planned improvements have been deployed.
