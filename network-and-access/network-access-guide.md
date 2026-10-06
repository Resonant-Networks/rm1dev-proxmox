<img src="mop/md/RNetlogo.jpg" alt="RNetlogo" class="logo" />

# Network Access Guide — rm1dev Infrastructure

| | |
|---|---|
| **Document Version:** | 1.0 |
| **Prepared By:** | Hafiz Mohd Rizal |
| **Date:** | July 2026 |

---

## 1. Infrastructure Changes

### 1.1 Summary of Changes

| Date | Change | Details |
|------|--------|---------|
| 2026-07-29 | Tailscale installed on Proxmox host `rm1dev` | Version 1.98.10, configured with `--netfilter-mode=off` |
| 2026-07-29 | IP forwarding enabled | `/etc/sysctl.d/99-tailscale.conf` — `net.ipv4.ip_forward = 1` |
| 2026-07-29 | Subnet routes advertised & approved | `192.168.0.0/24` and `10.90.39.0/24` via Proxmox host |
| 2026-07-29 | Config backup taken | `/root/pve-etc-backup-2026-07-29.tar.gz` (PVE config + network interfaces) |

### 1.2 Tailscale Configuration

**Proxmox host (`rm1dev`):**
```
tailscale up --advertise-routes=192.168.0.0/24,10.90.39.0/24 --netfilter-mode=off
```

**Client devices** (to use subnet routes via Proxmox):
```
tailscale up --accept-routes
```

### 1.3 Tailnet Details

| Property | Value |
|----------|-------|
| **Tailnet** | hafizmohdrizal@gmail.com |
| **MagicDNS Domain** | tail102e60.ts.net |
| **Admin Console** | https://login.tailscale.com/admin/machines |

### 1.4 Nodes on Tailnet

| Device | Tailscale IP | OS | Status |
|--------|-------------|----|--------|
| rm1dev (Proxmox host) | `100.118.216.78` | Linux | Active — subnet router |
| ubuntu-rm1dev (Ubuntu VM) | `100.80.103.95` | Linux | Active |
| laptop-iecun5n7-1 (Windows) | `100.67.205.111` | Windows | Active |
| laptop-iecun5n7 (Linux) | `100.91.6.49` | Linux | Offline |
| desktop-8fj10jt | `100.124.40.122` | Windows | Offline |
| iPad 9th Gen | `100.116.241.112` | iOS | Offline |
| oppo-reno11-5g | `100.71.231.13` | Android | Offline |
| izzah-1 | `100.114.61.58` | Linux | Offline |
| izzah | `100.127.55.91` | Windows | Offline |

---

## 2. Network Topology

### 2.1 Physical Layout

```
Internet
    │
    ├── Router/Gateway (192.168.0.1) — D-Link
    │
    ├── Dell PowerEdge R520 (rm1dev)
    │     ├── Proxmox VE — vmbr0: 192.168.0.101/24
    │     │                   vmbr1: 10.90.39.1/24  (isolated)
    │     │
    │     ├── VM 100 — ubuntu-rm1dev
    │     │     ├── ens18: 192.168.0.9/24  (via vmbr0)
    │     │     └── ens20: 10.90.39.104/24 (via vmbr1)
    │     │
    │     └── VM 101 — FNT-DEMO (stopped)
    │
    ├── ZPE Systems Nodegrid (OOB Mgmt) — 192.168.0.17
    │
    └── Client: laptop-iecun5n7 — 192.168.0.15
```

### 2.2 IP Address Reference

| Host | LAN IP | Tailscale IP | MagicDNS | Services |
|------|--------|-------------|----------|----------|
| **Proxmox host** | `192.168.0.101` | `100.118.216.78` | `rm1dev.tail102e60.ts.net` | SSH :22, Web :8006 |
| **Ubuntu VM** | `192.168.0.9` | `100.80.103.95` | `ubuntu-rm1dev.tail102e60.ts.net` | SSH :22 |
| **Ubuntu VM (2nd NIC)** | `10.90.39.104` | — | — | Internal network |
| **ZPE Nodegrid** | `192.168.0.17` | — | — | SSH :22, Web :443 |
| **Router** | `192.168.0.1` | — | — | Web :443 |
| **Windows Laptop** | `192.168.0.15` | `100.67.205.111` | `laptop-iecun5n7-1.tail102e60.ts.net` | — |

### 2.3 Subnet Routes (via Proxmox Tailscale)

| Subnet | Route Through | Purpose |
|--------|-------------|---------|
| `192.168.0.0/24` | `100.118.216.78` | LAN — router, Nodegrid, VMs, clients |
| `10.90.39.0/24` | `100.118.216.78` | Internal VM network |

---

## 3. Access Methods (MOP)

### 3.1 Access Matrix

| Target | Method | Over LAN | Over Tailscale (Remote) | Via SSH Tunnel |
|--------|--------|----------|------------------------|----------------|
| **Proxmox Web UI** | Browser | `https://192.168.0.101:8006` | `https://100.118.216.78:8006` | — |
| **Proxmox SSH** | Terminal | `ssh root@192.168.0.101` | `ssh root@100.118.216.78` | — |
| **Ubuntu VM SSH** | Terminal | `ssh ubuntu@192.168.0.9` | `ssh ubuntu@100.80.103.95` | — |
| **Nodegrid Web UI** | Browser | `https://192.168.0.17` | (via subnet route)* | `https://localhost:8443` after tunnel |
| **Nodegrid SSH** | Terminal | `ssh <user>@192.168.0.17` | `ssh <user>@192.168.0.17` (via subnet route) | `ssh -J root@100.118.216.78 <user>@192.168.0.17` |
| **Router Web UI** | Browser | `https://192.168.0.1` | `https://192.168.0.1` (via subnet route) | — |

*\* Nodegrid web UI may have IP access control enabled, blocking clients other than 192.168.0.101. Use SSH tunnel as workaround.*

### 3.2 One-Liner Commands

#### Proxmox
```bash
# SSH (LAN)
ssh root@192.168.0.101

# SSH (Tailscale / remote)
ssh root@100.118.216.78
ssh root@rm1dev.tail102e60.ts.net
```

#### Ubuntu VM
```bash
# SSH (LAN)
ssh ubuntu@192.168.0.9

# SSH (Tailscale / remote — direct)
ssh ubuntu@100.80.103.95
ssh ubuntu@ubuntu-rm1dev.tail102e60.ts.net
```

#### ZPE Nodegrid
```bash
# SSH (LAN — direct)
ssh admin@192.168.0.17

# SSH (Tailscale — via subnet route through Proxmox)
ssh admin@192.168.0.17

# SSH (double-hop through Proxmox — works even if subnet route is down)
ssh -J root@100.118.216.78 admin@192.168.0.17

# SSH tunnel for web UI access
ssh -L 8443:192.168.0.17:443 root@100.118.216.78
# Then open https://localhost:8443 in browser

# SSH tunnel through Tailscale directly
ssh -L 8443:192.168.0.17:443 root@100.118.216.78
# Then open https://localhost:8443
```

### 3.3 Quick Reference Card

```
┌──────────────────────────────────────────────────────────┐
│                      QUICK REFERENCE                      │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  TARGET          LAN                TAILSCALE            │
│  ───────         ───                ────────              │
│  Proxmox Web     .101:8006          100.118.216.78:8006  │
│  Proxmox SSH     root@.101          root@100.118.216.78  │
│  Ubuntu SSH      ubuntu@.9          ubuntu@100.80.103.95 │
│  Nodegrid SSH    admin@.17          admin@192.168.0.17   │
│  Nodegrid Web    .17:443            tunnel via Proxmox   │
│  Router          .1                 .1 (via subnet)      │
│                                                          │
│  PREFIX: 192.168.0.                                      │
└──────────────────────────────────────────────────────────┘
```

---

## 4. Prerequisites for Remote Access

### 4.1 Install Tailscale on Client Device

Download from https://tailscale.com/download or:

| OS | Command |
|----|---------|
| **Windows** | Download installer from tailscale.com or `winget install Tailscale.Tailscale` |
| **macOS** | `brew install --cask tailscale` or download from tailscale.com |
| **Linux** | `curl -fsSL https://tailscale.com/install.sh \| sh` |
| **iOS/Android** | Install from App Store / Play Store |

### 4.2 Enable Subnet Route Acceptance

After installing Tailscale and logging into your tailnet:

| OS | Method |
|----|--------|
| **Windows** | `tailscale up --accept-routes` (Admin terminal) |
| **macOS** | `sudo tailscale up --accept-routes` |
| **Linux** | `sudo tailscale up --accept-routes` |
| **iOS/Android** | Settings → toggle "Accept subnet routes" ON |
| **All devices** | Or: Admin console → Devices → select device → enable "Accept routes" |

---

## 5. Troubleshooting

### Symptom: Cannot reach LAN IPs over Tailscale

```
# Check client has accept-routes enabled
tailscale status

# Check subnet routes are approved on Proxmox (via API)
https://login.tailscale.com/admin/machines → rm1dev → verify routes approved

# Verify from Proxmox that routes are active
ssh root@192.168.0.101 "tailscale status --json" | grep PrimaryRoutes
```

### Symptom: Nodegrid web UI not loading (blank / timeout)

The ZPE Nodegrid may have IP access control filtering. Use SSH tunnel:

```bash
ssh -L 8443:192.168.0.17:443 root@100.118.216.78
```

Then access `https://localhost:8443` in browser.

### Symptom: Can't SSH into Ubuntu VM via Tailscale

```bash
# Connect via Proxmox first, then SSH to VM
ssh root@100.118.216.78
# From Proxmox:
ssh ubuntu@192.168.0.9

# Or add Tailscale to Ubuntu VM (already installed):
ssh ubuntu@100.80.103.95
```

---

## 6. Rollback

To remove Tailscale from the Proxmox host:

```bash
# Stop and disable
systemctl stop tailscaled
systemctl disable tailscaled

# Remove package
apt remove --purge tailscale

# Remove repo
rm /etc/apt/sources.list.d/tailscale.list
rm /usr/share/keyrings/tailscale-archive-keyring.gpg

# Remove IP forwarding config
rm /etc/sysctl.d/99-tailscale.conf
sysctl -w net.ipv4.ip_forward=0

# Restore config from backup if needed
tar xzf /root/pve-etc-backup-2026-07-29.tar.gz -C /
```

---

## Appendix A: Commands Used for Setup

```bash
# Backup Proxmox config
tar czf /root/pve-etc-backup-2026-07-29.tar.gz /etc/pve/ /etc/network/interfaces

# Add Tailscale repo (Debian 13 Trixie)
curl -fsSL https://pkgs.tailscale.com/stable/debian/trixie.noarmor.gpg \
  | tee /usr/share/keyrings/tailscale-archive-keyring.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/tailscale-archive-keyring.gpg] \
  https://pkgs.tailscale.com/stable/debian trixie main" \
  | tee /etc/apt/sources.list.d/tailscale.list

# Remove enterprise repos that require subscription
sed -i 's/^deb/#deb/' /etc/apt/sources.list.d/pve-enterprise.list
sed -i 's/^deb/#deb/' /etc/apt/sources.list.d/ceph.list

# Install Tailscale
apt update && apt install -y tailscale

# Start and authenticate
systemctl enable --now tailscaled
tailscale up --netfilter-mode=off
# [Visit URL printed to authenticate]

# Enable IP forwarding
echo 'net.ipv4.ip_forward = 1' > /etc/sysctl.d/99-tailscale.conf
sysctl -p /etc/sysctl.d/99-tailscale.conf

# Advertise subnet routes
tailscale up --advertise-routes=192.168.0.0/24,10.90.39.0/24 --netfilter-mode=off
```

## Appendix B: Hardware Reference

| Component | Details |
|-----------|---------|
| **Server Model** | Dell PowerEdge R520 |
| **Service Tag** | J3FSWX1 |
| **Proxmox Version** | 9.1.1 |
| **CPU** | 2x Intel Xeon E5-2470 v2 @ 2.40GHz (40 cores) |
| **RAM** | 125.8 GB |
| **Storage** | 66 GB boot + 136.5 GB LVM-thin + 5.5 TB LVM |
| **OOB Management** | ZPE Systems Nodegrid (192.168.0.17) |
