# Firewall rule too broad

## Problem

A permissive or misplaced firewall rule allows more sources or traffic than intended.

## Symptoms

Unexpected listener reachability, broad forwarding, or policy behavior that differs from the exposure plan. This is a defensive scenario, not a claim of a specific incident.

## Architecture / Context

UFW and iptables were used or investigated across IPv4, IPv6, VPS, gateway, and host boundaries.

## Hypotheses

Rule order; wrong interface; broad source CIDR; FORWARD instead of INPUT policy; IPv6 policy mismatch; NAT hiding source addresses.

## Investigation

List rules with counters and line numbers; compare to expected-exposure table; test from authorized internal and external sources.

## Commands Used

```bash
sudo ufw status verbose
sudo iptables -L -n -v --line-numbers
sudo ip6tables -L -n -v --line-numbers
ss -tulpn
```

## Root Cause

Rule-specific; inspect before changing or deleting rules.

## Solution

Replace broad access with explicit source, destination, protocol, and port policy. Preserve established traffic and recovery access.

## Verification

Check allowed and denied paths over IPv4 and IPv6 and ensure counters align with the test.

## Security Considerations

Remote firewall edits can lock out administration. Use a recovery path and avoid applying unreviewed snippets.

## What I Learned

Firewall intent must be checked against effective rules and actual reachability.
