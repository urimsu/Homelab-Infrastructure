# Security and disclosure

This repository describes a personal homelab and includes examples only. Do not copy a configuration into a live system without adapting its addresses, interfaces, routes, credentials, and firewall policy.

## Public repository rules

- Never commit passwords, private keys, API tokens, bot tokens, cookies, session data, or credential exports.
- Never publish real public IPs, personal email addresses, production domains, exact private addressing, or identifying hostnames.
- Use documentation-only IPv4 ranges (RFC 5737) in public-address examples and placeholders for environment-specific values.
- Keep local `.env` files and private configuration out of Git. Use `.env.example` only for variable names and harmless placeholders.
- Review the complete Git history before making a repository public; deleting a secret from the latest version does not remove it from earlier commits.

## Example configuration

Files under `configs/` are sanitized and incomplete by design. Placeholder values such as `<WG_PRIVATE_KEY>`, `<HOME_SUBNET>`, and `<SERVICE_IP>` must be replaced locally. Firewall and routing examples can interrupt connectivity or expose systems when adapted incorrectly.

## Reporting

For a suspected disclosure in this repository, remove public access to the affected credential or endpoint first, rotate/revoke the credential, and then investigate history and dependent systems. Do not report active secrets in a public issue. This repository does not provide a monitored security contact address.
