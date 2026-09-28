# Nextcloud

Nextcloud has been part of the self-hosting and cloud-service experimentation. Some experience also involved hosted Nextcloud, so this document does not claim every instance ran on the Proxmox host.

Areas explored include HTTPS, reverse proxying, DNS, storage capacity, sharing links, apps, document editing, and Collabora integration. A proxy deployment must configure the application's trusted domains and trusted proxy behavior correctly. Storage and backup claims are intentionally omitted because the available project facts do not establish a specific backup design.

For public sharing, consider link permissions and expiry settings. Keep administrative access private, patch the application and dependencies, and test storage growth. The reverse proxy and application are separate layers: validate each one independently.
