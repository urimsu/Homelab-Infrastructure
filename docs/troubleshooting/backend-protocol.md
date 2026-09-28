# Backend HTTP and HTTPS mismatch

## Problem

The proxy cannot communicate with a backend because it uses the wrong protocol or TLS expectations.

## Symptoms

Connection reset, handshake error, upstream failure, or 502 despite an apparently correct address and port.

## Architecture / Context

Reverse proxy → backend listener across LAN or WireGuard.

## Hypotheses

Proxy uses HTTPS against an HTTP listener (or vice versa); TLS certificate/SNI mismatch; wrong port; service redirect behavior.

## Investigation

Probe both schemes from the proxy host and inspect service configuration/logs. `curl -k` can isolate TLS verification as a diagnostic, but does not validate secure operation.

## Commands Used

```bash
curl -v http://<SERVICE_IP>:<PORT>/
curl -vk https://<SERVICE_IP>:<PORT>/
ss -tulpn
```

## Root Cause

Must be verified against the listener; no one protocol is assumed for every service.

## Solution

Set the upstream scheme and port to match the backend. Configure certificate trust and SNI if upstream TLS is intended.

## Verification

Verify backend directly with normal certificate validation where TLS is used, then check through the proxy.

## Security Considerations

Do not leave certificate verification disabled as a fix.

## What I Learned

Correct routing to the right port still fails when the protocol is wrong.
