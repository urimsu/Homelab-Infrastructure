# DNS and reverse proxy mismatch

## Problem

A service hostname resolves to an unexpected address or reaches the wrong proxy host.

## Symptoms

Wrong site, TLS name error, connection failure, or a request reaching an obsolete endpoint.

## Architecture / Context

DNS A/AAAA/CNAME records → VPS listener → proxy host selection → backend.

## Hypotheses

Stale resolver cache; incorrect A/AAAA; wildcard record; duplicate/conflicting records; wrong proxy hostname; DNS pointing to old address.

## Investigation

Query A and AAAA from the client and a trusted resolver. Compare the result with the intended public entry. Test the proxy with an explicit Host header after confirming reachability.

## Commands Used

```bash
dig A <DOMAIN>
dig AAAA <DOMAIN>
curl -v --resolve <DOMAIN>:443:<VPS_PUBLIC_IP> https://<DOMAIN>/
```

Use only placeholders in public docs; substitute your own values locally.

## Root Cause

Incident-specific; a hostname mismatch does not identify which DNS or proxy setting is wrong.

## Solution

Correct the record or proxy host that differs from the intended path and allow caches to expire.

## Verification

Test from the relevant resolver and over both address families, then confirm backend response.

## Security Considerations

Do not publish real domains or IPs. A wildcard can route unintended names to a public listener.

## What I Learned

DNS and proxy host selection are separate routing stages.
