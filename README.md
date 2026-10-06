# Resonant Networks — RM1Dev Proxmox Hypervisor Infrastructure (`rm1dev-proxmox`)

Welcome to the centralized source of truth for the **RM1Dev Bare-Metal Hypervisor** (`rm1dev`), running **Proxmox Virtual Environment (PVE)** across Resonant Networks.

---

## 📌 Executive Summary

**`rm1dev`** is the primary bare-metal virtualization host supporting core network applications, infrastructure management containers, and network element testbeds for Resonant Networks.

| Parameter | Value |
|---|---|
| **Server Model** | Dell PowerEdge R520 (2U Rackmount) |
| **Dell Service Tag** | `J3FSWX1` |
| **Hypervisor OS** | Proxmox VE 9.2 (Debian 13 Core, Linux 7.0.14-15-pve) |
| **Management IP** | `192.168.0.101` (LAN) / `100.118.216.78` (Tailscale) |
| **Web Console** | `https://192.168.0.101:8006/` |
| **Total Compute** | 2x Intel Xeon E5-2470 v2 @ 2.40 GHz (20 Cores / 40 vCPUs) |
| **System Memory** | 128 GB ECC DDR3 RAM (125.8 GB Usable) |
| **Primary Storage** | 250 GB Crucial MX500 SSD (OS + VMs) + 6.0 TB PERC H710 RAID Array |

---

## 🏛️ System & Network Architecture

```
                  ┌──────────────────────────────────────────────┐
                  │          Gateway Router (192.168.0.1)        │
                  └──────────────────────┬───────────────────────┘
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 │ Proxmox VE Host: rm1dev (192.168.0.101)       │
                 │ Tailscale Subnet Router: 100.118.216.78       │
                 │ Serial Console (COM2) ◄── ZPE Nodegrid (.17)  │
                 └───────────────┬──────────────────────┬────────┘
                                 │                      │
                                 │ (vmbr0 - LAN)        │ (vmbr1 - Isolated)
                                 ▼                      ▼
┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────┐
│ VM 100: rm1dev-control                       │  │ VM 101: FNT-DEMO                    │
│ ens18: 192.168.0.9 (vmbr0)                   │  │ ens18: 192.168.0.18 (vmbr0)         │
│ ens20: 10.90.39.104 (vmbr1)                  │  │ ens19: 10.90.39.2 (vmbr1)           │
│ Tailscale: 100.80.103.95                     │  │ Apache Tomcat (9090), Oracle (1521) │
│ Docker Host: Zabbix, Zammad, LibreNMS, OWUI  │  │ FNT Command Telco DCIM              │
└──────────────────────────────────────────────┘  └─────────────────────────────────────┘
```

---

## 💾 Storage & RAID Configuration

The host implements a dual-tier storage architecture managed by an integrated hardware RAID controller:

* **RAID Controller:** Dell PERC H710 Mini (`Broadcom / LSI MegaRAID SAS 2208 [Thunderbolt]`) with 512MB Battery-Backed Cache.
* **Tier 1 (High IOPS Boot & VMs):** Crucial MX500 250GB SATA SSD (`/dev/sdb`)
  * Storage ID `local`: Directory (`/var/lib/vz`) for ISOs, templates, and backups.
  * Storage ID `local-lvm`: LVM-Thin pool (`pve/data`, 136.5GB) hosting VM 100 and VM 101 disks.
* **Tier 2 (Bulk Capacity & PBS):** 6.0 TB SAS Virtual Drive (`/dev/sda`)
  * Formatted with GPT `ext4` labeled `storage6tb` mounted at `/mnt/pve/storage6tb`.
  * Dedicated for Proxmox Backup Server (PBS) datastores, template mirrors, and cold backups.
  * Driven by enterprise Toshiba 7200 RPM SAS drives (`MG04SCA40EN`, `MG03SCA300`).

---

## 🌐 Network Interfaces & Bridges

| Interface / Bridge | Type | IP / Subnet | Role & Uplink |
|---|---|---|---|
| **`vmbr0`** | Linux Bridge | `192.168.0.101/24` | Primary LAN bridge bridged to physical port `nic0` (`enp2s0f0`) |
| **`vmbr1`** | Linux Bridge | `10.90.39.1/24` | Isolated application bridge with `dnsmasq` DHCP service |
| **`nic1`** | Physical Port | `10.10.10.1/24` | Direct Ethernet link to Network Elements (`enp2s0f1`) |
| **`tailscale0`** | Mesh VPN | `100.118.216.78` | Subnet Router advertising `192.168.0.0/24` and `10.90.39.0/24` |

---

## 🖥️ Virtual Machine Fleet

| VMID | Name | OS | RAM | Disk | Status | Operating Role |
|---|---|---|---|---|---|---|
| **100** | `rm1dev-control` | Ubuntu 24.04 LTS | 50 GB | 100 GB | Running | Docker Host, Nginx Proxy, Zabbix/LibreNMS |
| **101** | `FNT-DEMO` | Oracle Linux 8.10 | 16 GB | 40 GB (IDE) | Running | FNT Command 14.4, Tomcat 10, Oracle DB |
| **200** | `opnsense-a` | FreeBSD / OPNsense | 4 GB | 16 GB | Stopped | Standby Firewall / IPsec Gateway A |
| **201** | `opnsense-b` | FreeBSD / OPNsense | 20 GB | 16 GB | Stopped | Standby Firewall / IPsec Gateway B |

---

## 📂 Repository Structure

```
rm1dev-proxmox/
├── README.md                                  # Master index and host architecture overview (this file)
├── .gitignore                                 # Clean gitignore
│
├── hardware-and-specifications/               # Bare-metal specifications and inspection reports
│   ├── host-hardware-specification.md         # Comprehensive hardware inventory and topology
│   ├── proxmox-report.md                      # Full Proxmox VE host inspection report
│   ├── proxmox-report.pdf                     # PDF export of host inspection report
│   ├── Proxmox_Host_Configuration_Detailed_Report.docx # Formatted DOCX report
│   └── Infrastructure_Documentation_Report.docx # Enterprise infrastructure architecture doc
│
├── storage-and-raid/                          # Storage architecture, RAID controllers & pools
│   ├── raid-controller-configuration.md       # Dell PERC H710 Mini specs, physical drives, smartctl
│   ├── proxmox_pbs_6tb_plan.md                # 6TB storage conversion & PBS datastore runbook
│   └── storage-pools.md                       # Storage layout (/var/lib/vz, local-lvm, storage6tb)
│
├── installation-and-mops/                     # Installation procedures, SOPs, and MOPs
│   ├── proxmox-virtual-media-installation-sop.md # Bare-metal install SOP via Virtual Media / HTML5
│   ├── Proxmox_VE_Virtual_Media_Installation_Guide.docx # DOCX SOP export
│   ├── mop-provision-proxmox-into-zabbix.md   # MOP: Registering rm1dev into Zabbix agent2
│   └── mop-idrac-ipmi-configuration.md        # MOP: IPMI/BMC static IP via ipmitool
│
├── network-and-access/                        # Network topology, bridges, and access methods
│   ├── network-topology-and-bridges.md        # vmbr0, vmbr1, nic1, NAT port-forwards, Tailscale
│   └── network-access-guide.md                # Complete network access guide & one-liners
│
├── change-logs-and-history/                   # Chronological maintenance history
│   ├── changes-and-maintenance-history.md     # Timeline of all structural changes to rm1dev
│   ├── 01_initial-system-setup.md             # Base OS and initial configuration
│   ├── 06_nginx-reverse-proxy.md              # Reverse proxy configuration
│   ├── 07_tailscale-subnet-advertise.md       # Subnet router setup
│   ├── 09_fnt-deployment.md                   # FNT VM import and IDE disk adaptation
│   └── 2026-08-04_1626_provision-ubuntu-rm1dev-zabbix.md # Zabbix provisioning log
│
├── vm-inventory/                              # Virtual machine allocations
│   └── vm-and-software-inventory.md           # Full VM, container, and IPAM allocation registry
│
└── tooling-and-mcp/                           # Model Context Protocol (MCP) integrations
    ├── README.md                              # MCP server capabilities and configuration
    ├── proxmox_mcp_stdio.py                   # Stdio transport MCP server
    └── proxmox_mcp_sse.py                     # SSE transport MCP server
```

---

## 🔒 Security Guidelines

* This repository is maintained as a **public** engineering reference for Resonant Networks.
* **Never commit active production passwords, API token secrets, or private SSH keys.**
* Access to Proxmox VE Web UI and SSH is restricted to authorized engineers via Tailscale and the local management subnet.

---

## 👥 Maintainers & Contributors

* **Resonant Networks Infrastructure & NOC Team**
* **Repository:** [https://github.com/Resonant-Networks/rm1dev-proxmox](https://github.com/Resonant-Networks/rm1dev-proxmox)
