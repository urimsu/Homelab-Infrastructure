# IPv4 blocked while IPv6 remains reachable

## Problem

A service appears closed over IPv4 but remains reachable over IPv6.

## Symptoms

IPv4 tests fail while an AAAA record or IPv6 listener permits access. This is a security validation scenario, not a claim of a specific exposure incident.

## Architecture / Context

Host firewall, router/provider edge, DNS A/AAAA, and service sockets all affect reachability.

## Hypotheses

IPv6 firewall disabled or permissive; service bound to `::`; AAAA points to an active address; router IPv6 policy differs from IPv4 policy.

## Investigation

Inspect listeners and DNS. Run authorized tests over both address families from an external system you control. Review host and edge firewall rules separately.

## Commands Used

```bash
ss -tulpn
dig A <DOMAIN>
dig AAAA <DOMAIN>
ip -6 addr
ip -6 route
```

Use `nmap -6` only against infrastructure you own or are authorized to assess.

## Root Cause

Depends on the host and edge policy; verify before attributing a cause.

## Solution

Apply equivalent least-exposure policy to IPv6 or disable an unnecessary listener/record through a deliberate change.

## Verification

Confirm expected results for IPv4 and IPv6 from an authorized external vantage point.

## Security Considerations

Do not assume NAT provides an IPv6 firewall. Check both protocol families.

## What I Learned

IPv4 reachability tests cannot establish IPv6 exposure.
