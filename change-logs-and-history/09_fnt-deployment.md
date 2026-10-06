# DevOps Log — FNT Command Appliance Deployment

## 2026-06-25 20:11 UTC — Proxmox Deployment & Remote Access

### Objective
Deploy FNT Command Appliance (Oracle Linux 8.10, 14.4.1) from ESXi OVA to Proxmox, accessible remotely via Tailscale + nginx proxy — no SSH tunneling.

### Architecture (Final)

```
Remote Engineer (Tailscale, any device)
    │  https://demo-ref.fntgrp.com/app/command/
    │  hosts: 100.80.103.95 demo-ref.fntgrp.com
    ▼
ubuntu-rm1dev (nginx proxy — Tailscale 100.80.103.95)
    │  route: 10.90.39.0/24 via 192.168.0.101
    ▼
Proxmox (192.168.0.101, ip_forward enabled, DHCP on vmbr1)
    │
    ▼
FNT Appliance (10.90.39.2)
    ├─ Port 9090 — FNT Command (Tomcat, `/app/command/`)
    └─ Port 9190 — FNT StagingArea (Tomcat, `/stagingarea/`)
```

### Setup Log

| Step | Action | Issue | Fix |
|------|--------|-------|-----|
| 1 | SCP VMDK (14GB) to Proxmox | — | Done |
| 2 | `qm importdisk` to local-lvm | Rootfs 100% full (partial qcow2 + VMDK left behind) | Cleaned stale files |
| 3 | Attach disk as SATA | Blank console — initramfs lacks AHCI driver | Changed to **IDE** (`ide0`) — matches OVF spec |
| 4 | Boot VM | No DHCP on isolated bridge vmbr1 | Installed **dnsmasq** on Proxmox, static lease `10.90.39.2` |
| 5 | Add nginx proxy on ubuntu-rm1dev | No route to 10.90.39.x | Enabled **ip_forward** on Proxmox, static route on ubuntu-rm1dev |
| 6 | FNT Command 404 | Wrong context path | Tomcat context is `/app/command/` not `/app/` |
| 7 | Windows can't resolve | Hosts file had `127.0.0.1 demo-ref.fntgrp.com` (from Docker) — overrode Tailscale entry | Deleted stale entry, used `100.80.103.95` |
| 8 | FNT UI greyed out | License JS checks `window.location.hostname` against `demo-ref.fntgrp.com` | Users access via `demo-ref.fntgrp.com` (hosts entry) |

### Current State

**VM 101 — FNT-DEMO** (Running)
- 4 vCPU, 16GB RAM, 40GB IDE disk
- `10.90.39.2` (static DHCP on vmbr1)
- Services: SSH, Oracle DB (1521), Tomcat (9090/9190), VNC (5901)
- StagingArea: ✅ fully working
- FNT Command: ✅ working (license OK when accessed via correct hostname)

### Access

| Application | URL |
|-------------|-----|
| FNT Command | `https://demo-ref.fntgrp.com/app/command/` |
| FNT StagingArea | `https://demo-ref.fntgrp.com/stagingarea/` |

Prerequisites: Tailscale connected, hosts entry `100.80.103.95 demo-ref.fntgrp.com`, accept self-signed cert.

### Credentials

| System | Username | Password |
|--------|----------|----------|
| Linux root (FNT VM) | `root` | `DemoRef!FnT` |
| FNT Command | `command` | `command` |
| FNT StagingArea (Admin) | `superuser` | `fnt@SGA8` |
| FNT StagingArea (Demo) | `stagingarea` | `fnt@SGA7` |
| License Admin | `licadmin` | `LicAdmin!FnT` |

### MOP

`/home/ubuntu/devops-logs/MOP_remote-engineer-fnt-access.md`

