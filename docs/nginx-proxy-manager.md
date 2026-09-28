# Nginx Proxy Manager

Nginx Proxy Manager was explored as a simpler interface for managing proxy hosts and certificates after manual Nginx configuration made the underlying concepts clearer. Its public proxy listeners and its administration interface are different surfaces.

- Proxy hosts can serve selected application endpoints.
- Certificates and hostnames must match the intended DNS and backend.
- WebSocket support may be required by an application.
- Access lists can add restrictions but do not replace network firewall policy.
- The administration interface should be reachable only over the LAN or VPN.

The management port varies with installation and must be verified locally; no port mapping is claimed here. For a `502`, trace proxy-to-backend connectivity before changing DNS. See [reverse proxy](reverse-proxy.md) and the [502 investigation](troubleshooting/reverse-proxy-502.md).
