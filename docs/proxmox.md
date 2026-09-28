# Proxmox VE

Proxmox VE is the virtualization layer on the Fujitsu PRIMERGY TX200 S7. It provides the host management plane and runs virtual machines and LXC containers for self-hosting experiments.

## Hardware context

- 2 × Intel Xeon E5-2420 processors, 6 cores per socket (12 physical cores, 24 logical CPUs).
- SAS storage behind a hardware RAID controller; observed capacities were approximately 836 GB and 476 GB. The exact layer represented by those capacity readings is not established here.
- RAID level and final logical-volume layout are not confirmed and are intentionally omitted.

## Networking and guests

Proxmox bridge networking connects guests to the host's network interfaces. A bridge is a Layer 2 connection point; guest addressing, upstream routing, firewall policy, and VLAN support (if any) are separate configuration questions. No VLAN deployment is claimed here.

VMs provide a separate kernel and stronger isolation boundary than LXC containers, which share the host kernel. Both are useful for learning, but their operational and security characteristics differ. Keep host management reachable only from the trusted LAN or VPN path.

## Storage layers

```text
Physical SAS disk → RAID controller → controller logical volume
→ Linux block device → Proxmox storage definition → guest disk
```

This distinction helped avoid treating a disk reported by the controller as if it were directly the guest's storage. Confirm the controller's logical volumes and Proxmox storage configuration before changing disks.

## Administration and operations

The web interface commonly uses TCP 8006, but this is a documentation example and says nothing about public exposure. SSH and the web UI belong on the management network or VPN. Monitoring, Wake-on-LAN, and controlled shutdown are documented in [monitoring](monitoring.md), [Wake-on-LAN](wake-on-lan.md), and [energy management](energy-management.md).

Before shutdown, account for guest workloads and use a controlled host shutdown. Automation should have command-specific privileges rather than unrestricted sudo access.
