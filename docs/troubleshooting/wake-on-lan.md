# Wake-on-LAN troubleshooting

## Problem

The Proxmox host does not start after a Wake-on-LAN request.

## Symptoms

The sender reports success but the host remains unavailable. Sending a packet is not confirmation of boot.

## Architecture / Context

Authorized operator → Raspberry Pi → home broadcast domain → Proxmox NIC.

## Hypotheses

Wrong MAC; BIOS/NIC wake setting disabled; unsupported power state; no link power; broadcast not forwarded across subnet; target network mismatch.

## Investigation

Verify MAC on the local LAN, check BIOS/UEFI and NIC state, send from the same broadcast domain, and observe link/boot state. Consider switch/router behavior.

## Commands Used

```bash
ip neigh
ethtool <INTERFACE>
python3 scripts/wake-on-lan/wol.py
```

Hardware support varies; command availability depends on the OS.

## Root Cause

No single historical failure is asserted; check each hardware and network condition.

## Solution

Correct the configured MAC/broadcast or enable supported wake behavior in firmware/NIC settings.

## Verification

After sending, check for host boot and an authorized service response.

## Security Considerations

Keep the MAC private where identifying hardware is a concern. Restrict who can trigger automation.

## What I Learned

Wake-on-LAN depends on firmware, power state, and Layer 2 delivery as well as script correctness.
