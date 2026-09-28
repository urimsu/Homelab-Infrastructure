# Raspberry Pi infrastructure node

The Raspberry Pi has been used for WireGuard routing, Pi-hole DNS filtering, Wake-on-LAN, and SSH/Discord automation experiments. Available memory was about 1.8 GiB. Its role grew from small utility tasks into a network dependency, which makes lifecycle and recovery planning important.

## Operational considerations

- Keep its OS and packages on a supported release.
- Monitor storage, memory, and service availability.
- Treat gateway or DNS failure as a possible loss of remote access; retain a safe local recovery path.
- Keep private keys and bot tokens outside the repository.
- Give SSH automation narrow command permissions.

An older Raspberry Pi OS / Debian Buster environment encountered repository errors associated with an end-of-life distribution. Archive repositories may help retrieve old packages for recovery, but should not turn an exposed EOL installation into a long-term operating state. Upgrade to a supported release and verify application compatibility.

See the [repository troubleshooting note](troubleshooting/raspberry-pi-repositories.md), [Pi-hole](pihole.md), and [Wake-on-LAN](wake-on-lan.md).
