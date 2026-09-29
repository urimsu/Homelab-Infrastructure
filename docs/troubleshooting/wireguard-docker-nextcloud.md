# Troubleshooting: Nextcloud behind Nginx Proxy Manager + WireGuard

## Problem

My Nextcloud instance is hosted inside my home network:

- Nextcloud: `192.168.0.11`
- WireGuard Gateway: `192.168.0.21`
- WireGuard VPN network: `10.0.0.0/24`
- VPS WireGuard address: `10.0.0.1`
- Nginx Proxy Manager: Docker container on VPS
- Docker network: `172.18.0.0/16`

The public domain points to the VPS, where Nginx Proxy Manager forwards
requests through WireGuard to the Nextcloud server.

Architecture:

Internet
   |
   v
VPS / Nginx Proxy Manager
   |
   | WireGuard
   v
WireGuard Gateway
   |
   v
Home LAN
   |
   v
Nextcloud


## Symptoms

Nextcloud was reachable directly via its local IP:

    https://192.168.0.11

However, access through the public domain failed.

DNS resolution was correct and the domain pointed to the VPS.

The VPS itself could also reach Nextcloud:

    curl -vk https://192.168.0.11

But requests through Nginx Proxy Manager did not complete.


# Step 1 - Verify WireGuard routing

The VPS routing table contained:

    192.168.0.0/24 dev wg0

Therefore traffic destined for the home LAN was correctly routed through
the WireGuard tunnel.

Tests:

    ping 192.168.0.11

worked.

However:

    curl -vk https://192.168.0.11

initially stalled during the TLS handshake.


# Step 2 - Discover MTU problem

Large ICMP packets failed:

    ping -M do -s 1372 -c 3 192.168.0.11

Result:

    100% packet loss

Smaller packets worked:

    ping -M do -s 1200 -c 3 192.168.0.11

Result:

    0% packet loss

This indicated a Path MTU problem.


## What is MTU?

MTU stands for:

    Maximum Transmission Unit

It defines the maximum packet size that can be transmitted over a network
interface without fragmentation.

Ethernet commonly uses an MTU of 1500 bytes.

WireGuard adds additional headers for encryption and tunneling. Therefore,
the packet transported inside WireGuard must be smaller than the physical
network's maximum packet size.

If the MTU is too large, small packets such as ICMP or TCP handshakes may
work while larger packets fail.

This can produce symptoms such as:

- websites loading extremely slowly
- TLS handshakes hanging
- VPN connections appearing connected but behaving unreliably
- small pings working while larger packets fail


## Solution

The WireGuard MTU was reduced to:

    MTU = 1280

in:

    /etc/wireguard/wg0.conf

After restarting WireGuard:

    systemctl restart wg-quick@wg0

HTTPS communication between the VPS and Nextcloud worked correctly.


# Step 3 - Isolate the Docker problem

Even after fixing the WireGuard MTU, the public domain still did not work.

The VPS itself could reach Nextcloud:

    curl -vk https://192.168.0.11

Result:

    HTTP/1.1 302 Found

But the Nginx Proxy Manager Docker container could not:

    docker exec nginx-proxy-manager \
        curl -vk --connect-timeout 10 https://192.168.0.11

Result:

    Connection timed out

This was the key diagnostic result.

It proved that:

    VPS -> WireGuard -> Nextcloud

worked, while:

    Docker -> VPS -> WireGuard -> Nextcloud

did not.


# Step 4 - Identify the Docker network

Running:

    ip route

showed the Docker bridge network:

    172.18.0.0/16

Nginx Proxy Manager therefore did not originate its connections directly
from the VPS WireGuard interface.

Its traffic originated from a separate Docker network.


# Step 5 - Allow Docker -> WireGuard forwarding

The VPS acts as a router between the Docker network and the WireGuard
network.

Forwarding from Docker to the home LAN was explicitly allowed:

    iptables -I FORWARD 1 \
      -s 172.18.0.0/16 \
      -d 192.168.0.0/24 \
      -o wg0 \
      -j ACCEPT

Return traffic was allowed only for existing connections:

    iptables -I FORWARD 1 \
      -s 192.168.0.0/24 \
      -d 172.18.0.0/16 \
      -i wg0 \
      -m conntrack \
      --ctstate ESTABLISHED,RELATED \
      -j ACCEPT


# Step 6 - NAT Docker traffic

The Docker network only exists internally on the VPS.

Devices in the home LAN do not necessarily have a route back to:

    172.18.0.0/16

Therefore source NAT was added:

    iptables -t nat -I POSTROUTING 1 \
      -s 172.18.0.0/16 \
      -d 192.168.0.0/24 \
      -o wg0 \
      -j MASQUERADE

Conceptually this changes traffic from:

    172.18.x.x -> 192.168.0.11

into traffic appearing to originate from the WireGuard side of the VPS.

Connection tracking automatically translates the response back to the
Docker container.


# Final Traffic Flow

The final working path is:

    Client
      |
      v
    nextcloud.example.com
      |
      v
    VPS :443
      |
      v
    Docker
      |
      v
    Nginx Proxy Manager
    172.18.x.x
      |
      | FORWARD + NAT
      v
    WireGuard (wg0)
    10.0.0.1
      |
      | encrypted tunnel
      v
    WireGuard Gateway
    10.0.0.10
      |
      v
    Home LAN
    192.168.0.0/24
      |
      v
    Nextcloud
    192.168.0.11:443


# Lessons Learned

The most important lesson was to test each network layer independently.

Instead of treating "the website does not work" as one problem, the path
was divided into individual components:

    DNS                         -> OK
    Public VPS :443             -> OK
    TLS certificate             -> OK
    WireGuard handshake         -> OK
    VPS -> Home LAN             -> OK after MTU fix
    Nextcloud HTTPS             -> OK
    Docker -> Home LAN          -> FAILED
    Docker forwarding/NAT       -> FIXED

A successful connection from the host does not automatically mean that a
Docker container can reach the same destination.

Docker containers use their own virtual networks and forwarded traffic
passes through different firewall paths than traffic generated directly
by the host.

Another important lesson was that a working WireGuard handshake does not
guarantee that all traffic through the tunnel works correctly. MTU issues
can allow small packets while silently breaking larger HTTPS/TLS traffic.
