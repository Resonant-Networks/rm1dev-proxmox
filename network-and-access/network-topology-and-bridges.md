# RM1Dev — Network Topology, Bridges & Subnet Routing

## 1. Physical & Virtual Network Topology

```
                  ┌──────────────────────────────────────────────┐
                  │          Gateway Router (192.168.0.1)        │
                  └──────────────────────┬───────────────────────┘
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 │ Proxmox VE Host: rm1dev (192.168.0.101)       │
                 │ Tailscale Mesh Router: 100.118.216.78         │
                 └───────────────┬──────────────────────┬────────┘
                                 │                      │
                                 │ (vmbr0 - LAN)        │ (vmbr1 - Isolated)
                                 ▼                      ▼
┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────┐
│ VM 100: rm1dev-control                       │  │ VM 101: FNT-DEMO                    │
│ ens18: 192.168.0.9 (vmbr0)                   │  │ ens18: 192.168.0.18 (vmbr0)         │
│ ens20: 10.90.39.104 (vmbr1)                  │  │ ens19: 10.90.39.2 (vmbr1)           │
│ Tailscale: 100.80.103.95                     │  │ Apache Tomcat (9090), Oracle (1521) │
└──────────────────────────────────────────────┘  └─────────────────────────────────────┘
```

---

## 2. Linux Bridges Configuration (`/etc/network/interfaces`)

### 2.1 Bridge 0: Management & Physical LAN (`vmbr0`)
* **Subnet:** `192.168.0.0/24`
* **Host IP:** `192.168.0.101`
* **Default Gateway:** `192.168.0.1`
* **Bridge Ports:** `nic0` (`enp2s0f0` — Broadcom BCM5720 Gigabit)
* **NAT / Port Forwarding:**
  ```bash
  # Port forward shortcut for local browser access to Network Element
  post-up iptables -t nat -A PREROUTING -i vmbr0 -p tcp --dport 8443 -j DNAT --to-destination 10.10.10.3:443
  post-down iptables -t nat -D PREROUTING -i vmbr0 -p tcp --dport 8443 -j DNAT --to-destination 10.10.10.3:443
  ```

### 2.2 Bridge 1: Isolated Application Subnet (`vmbr1`)
* **Subnet:** `10.90.39.0/24`
* **Host IP:** `10.90.39.1`
* **Bridge Ports:** None (Software virtual switch only)
* **DHCP Server:** Managed by host `dnsmasq` instance with static leases:
  * `10.90.39.2` → `bc:24:11:a2:5b:64` (VM 101 `FNT-DEMO`)
  * `10.90.39.104` → `bc:24:11:48:4c:d1` (VM 100 `rm1dev-control`)

### 2.3 Direct Network Element Interface (`nic1`)
* **Physical Port:** `enp2s0f1`
* **IP Address:** `10.10.10.1/24`
* **Role:** Dedicated direct physical Ethernet patch link to hardware Network Element (e.g. ADVA ALM optical monitoring device).

---

## 3. Tailscale Subnet Router & IP Forwarding

The Proxmox host operates as the central Tailscale Subnet Router for the entire RM1 Lab.

### 3.1 Kernel IP Forwarding
Enabled in `/etc/sysctl.d/99-tailscale.conf` (or `/etc/sysctl.conf`):
```ini
net.ipv4.ip_forward = 1
net.ipv6.conf.all.forwarding = 1
```

### 3.2 Advertised Routes
Run on `rm1dev`:
```bash
tailscale up --advertise-routes=192.168.0.0/24,10.90.39.0/24 --accept-routes
```
* `192.168.0.0/24`: Grants remote access to the host, Ubuntu VM, router, and ZPE Nodegrid.
* `10.90.39.0/24`: Grants direct access to VM 101 FNT Command and isolated database interfaces.
