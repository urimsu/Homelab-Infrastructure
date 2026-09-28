# Reverse proxy

The project moved from manually configured Nginx toward Nginx Proxy Manager after learning the request path and proxy concepts. The intended flow is:

```text
Internet client → VPS HTTPS listener → reverse proxy
→ WireGuard route → selected internal service
```

A proxy routes requests by hostname and forwards them to a backend. It does not repair DNS, routes, backend availability, or firewall policy. Test backend connectivity from the proxy host before investigating certificates or public DNS.

## Manual Nginx example

See [reverse-proxy.conf.example](../configs/nginx/reverse-proxy.conf.example). It uses a placeholder domain and backend. TLS certificate paths are deliberately left as placeholders. Validate forwarded headers and trusted proxy settings with the application; do not trust arbitrary client-supplied forwarding headers.

## Public and private listeners

Selected application hosts may be public over HTTPS. Proxy administration and infrastructure management remain private/VPN-only. Use separate DNS names and access policy where appropriate, and verify the actual sockets and firewall rules.

## Backend protocol

Use HTTP or HTTPS according to the backend's actual listener. A scheme mismatch can fail even when routing works. For TLS backends, certificate validation and SNI may matter; `curl -k` is a diagnostic aid only and must not become a production validation bypass.
