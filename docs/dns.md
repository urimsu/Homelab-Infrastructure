# DNS and domains

DNS names map clients to an address; they do not prove that a service is listening or that a route to it works. Production domains are intentionally omitted. Examples use `service.example.com`, `status.example.com`, and `cloud.example.com`.

## Record types

- **A** maps a name to IPv4.
- **AAAA** maps a name to IPv6.
- **CNAME** aliases a name to another DNS name. A CNAME cannot coexist with other record types at the same owner name (apart from DNSSEC-related records).
- Wildcard records can simplify name resolution but do not configure proxy hosts or certificates by themselves.

Check both address families and the resolver actually used by a VPN client. A private DNS response can differ from a public one. For a reverse-proxy failure, test the backend address and port directly before modifying DNS.

```bash
dig A service.example.com
dig AAAA service.example.com
curl -v https://service.example.com/
```

Replace example names only in private local configuration. Never commit personal domains or DNS provider credentials.
