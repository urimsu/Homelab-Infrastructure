# Raspberry Pi OS repository errors

## Problem

Package operations on an older Raspberry Pi OS / Debian Buster installation returned repository errors.

## Symptoms

Package indexes or downloads fail because the distribution release is no longer served from normal mirrors.

## Architecture / Context

The Raspberry Pi had an older OS while performing gateway, DNS, and automation duties. Exact package failure details varied and are not reproduced as a single transcript.

## Hypotheses

End-of-life repository moved to archive; stale package lists; DNS/network issue; incompatible third-party repository.

## Investigation

Check OS release, repository URLs, DNS, and system time. Distinguish mirror failure from local connectivity. Confirm the distribution support status before changing sources.

## Commands Used

```bash
cat /etc/os-release
apt update
getent hosts <REPOSITORY_HOST>
```

## Root Cause

The legacy release had reached end of life; repository availability was part of the observed issue.

## Solution

Prefer a supported OS upgrade and validate compatibility of WireGuard, Pi-hole, and automation. Archive repositories can support temporary recovery, but do not make an exposed EOL system a long-term operating state.

## Verification

After upgrading, run package updates and check service status, routing, and DNS behavior.

## Security Considerations

Unsupported systems stop receiving normal security fixes. Reduce exposure and prioritize migration.

## What I Learned

OS lifecycle is an infrastructure dependency, not just a package-manager detail.
