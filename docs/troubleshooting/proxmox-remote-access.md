# Proxmox is not reachable remotely

## Problem

Proxmox management is unavailable to a remote administrator.

## Symptoms

The management UI or SSH works locally but not from VPN. This is expected if there is no route; it should not be solved by exposing management directly to the Internet.

## Architecture / Context

Remote administrator → WireGuard → home gateway → management LAN → Proxmox. The web UI commonly uses TCP 8006.

## Hypotheses

VPN peer routes omit the management subnet; gateway forwarding/firewall issue; return route absent; Proxmox host firewall; wrong address; service unavailable.

## Investigation

Check local service, listener, VPN handshake, routes, forwarding, and firewall at each hop. Test a known management address only after VPN is up.

## Commands Used

```bash
ss -tulpn
ip route
wg
curl -vk https://<PROXMOX_IP>:8006/
```

## Root Cause

Must be determined from the specific route and service state; no unique past cause is asserted.

## Solution

Restore the intended VPN route and narrowly permit management traffic. Do not publish the UI as a shortcut.

## Verification

Confirm UI access over VPN and confirm it is not reachable from an unauthorized public path.

## Security Considerations

Proxmox administration is a high-impact control plane. Use VPN and strong authentication.

## What I Learned

Remote administration availability should be designed as a private path.
