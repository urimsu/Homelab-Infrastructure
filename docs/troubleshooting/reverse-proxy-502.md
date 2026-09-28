# Reverse proxy returns 502 Bad Gateway

## Problem

A proxied service displays `502 Bad Gateway`, sometimes with an `openresty` response.

## Symptoms

The proxy receives a client request but cannot produce a valid response from the configured upstream. Several causes are possible; the exact historical cause is not established as universal.

## Architecture / Context

Client → VPS/reverse proxy → WireGuard → selected backend.

## Hypotheses

Backend offline; wrong IP or port; HTTP/HTTPS mismatch; proxy route blocked by VPN or firewall; service bound only to localhost; container path issue; TLS validation/SNI issue.

## Investigation

Test the backend locally, then from the proxy host. Confirm the listening socket and route. Inspect WireGuard and firewall state. Only after direct backend reachability works should DNS and proxy host configuration be changed.

## Commands Used

```bash
curl -v http://<BACKEND_IP>:<PORT>/
curl -vk https://<BACKEND_IP>:<PORT>/
ss -tulpn
ip route
wg
systemctl status <SERVICE_NAME>
```

## Root Cause

Multiple hypotheses were relevant; do not infer one from the 502 text alone.

## Solution

Correct the specific failed layer: start/fix the backend, use its actual protocol and port, repair the route/firewall, bind it to a reachable interface, or configure TLS correctly.

## Verification

Check direct backend response from the proxy host, then request via the proxy, then resolve and test the public hostname over IPv4 and IPv6 as applicable.

## Security Considerations

`curl -k` skips certificate verification and is diagnostic only. Keep admin hosts private and avoid exposing backend ports publicly.

## What I Learned

A 502 is a symptom at the proxy boundary, not a diagnosis. Trace the request hop by hop.
