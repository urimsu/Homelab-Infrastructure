# Service works locally but not remotely

## Problem

A service responds from its own host but a remote client cannot connect.

## Symptoms

Local curl succeeds while a request from another host times out or is refused. Historical cases may differ; no single root cause is claimed.

## Architecture / Context

Service host → LAN/VPN route → client or proxy. The service may be on a VM, container, or physical host.

## Hypotheses

Loopback-only bind; host firewall; guest bridge/network configuration; missing route; VPN policy; upstream firewall; wrong destination address or port.

## Investigation

Inspect bind address and socket. Test from the same subnet, then from gateway, VPN peer, and proxy. Compare resolved address and route. Check both IPv4 and IPv6.

## Commands Used

```bash
curl -v http://127.0.0.1:<PORT>/
ss -tulpn
ip addr
ip route
curl -v http://<SERVICE_IP>:<PORT>/
```

## Root Cause

Must be established for the specific incident; local success only rules out some application failures.

## Solution

Fix the identified bind, route, or firewall layer with the narrowest required change.

## Verification

Repeat tests from each network boundary and verify no unintended public listener appeared.

## Security Considerations

Binding to all interfaces can increase exposure. Permit only trusted source networks.

## What I Learned

Local functionality and network reachability are separate properties.
