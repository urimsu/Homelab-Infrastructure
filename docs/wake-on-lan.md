# Wake-on-LAN

Wake-on-LAN was used or explored as a way to bring the Proxmox host online when needed, reducing the time the server must run continuously.

```mermaid
sequenceDiagram
  participant U as Authorized operator
  participant P as Raspberry Pi
  participant N as Home network
  participant S as Proxmox server
  U->>P: Request wake operation
  P->>N: Send magic packet to configured broadcast domain
  N->>S: Deliver packet to NIC (if powered/configured)
  S-->>U: Host becomes reachable after boot
```

Wake-on-LAN depends on NIC and BIOS/UEFI support, the system's power state, link state, and whether the magic packet crosses the network path. Routers commonly do not forward broadcast packets across subnets. Validate the target MAC locally and keep it out of public documentation.

The example [wol.py](../scripts/wake-on-lan/wol.py) requires an environment-provided MAC and broadcast address. It validates input and reports errors. This script sends a packet; it does not confirm that the server booted. Verify afterward with an authorized service check.
