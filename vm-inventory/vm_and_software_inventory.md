# Infrastructure & Software Inventory Documentation
**Directive**: HQ System Inventory Requirement  
**Document Generated**: 2026-08-11  
**Scope**: All Virtual Machines, Containerized Applications, System Tooling, Networks & Credentials  

---

## 📌 Executive Summary & System Overview

| Parameter | Value / Detail |
| :--- | :--- |
| **Primary Hypervisor** | Dell PowerEdge R520 (`rm1dev`) |
| **Hypervisor Platform** | Proxmox VE 8.x |
| **Production Go-Live Date** | **2026-08-07** (Initial Provisioning: 2026-08-04) |
| **Primary Network Subnet** | `192.168.0.0/24` (Default Gateway: `192.168.0.1`) |
| **Isolated App Subnet** | `10.90.39.0/24` (Gateway: `10.90.39.1`) |
| **Tailscale Subnet Router** | `100.118.216.78` (`rm1dev`) / `100.80.103.95` (`ubuntu-rm1dev`) |

---

## 🖥️ 1. Virtual Machine (VM) Inventory

### VM 100: `ubuntu-rm1dev` (Management & Container Host)

```yaml
1) Software Versions:
   - Operating System: Ubuntu 24.04 LTS (Noble Numbat)
   - Linux Kernel: 6.8.0-31-generic x86_64
   - Container Engine: Docker 26.x / Docker Compose v2.x
   - Runtime Tools: Python 3.11 / 3.14, Node.js 20, Nginx 1.25.5
   - Monitoring Agent: Zabbix Agent2 (1:6.4.21-1+ubuntu24.04 pinned)

2) Hardware / Resource Allocation:
   - CPU: 8 vCPUs (Intel Xeon E5 Series)
   - Memory (RAM): 50.0 GB Total (47.55 GB active)
   - Disk Storage: 100.0 GB LVM (`/dev/mapper/ubuntu--vg-ubuntu--lv` on `/`)

3) Credentials & Access (UID / Password):
   - Host SSH User: ubuntu (SUDO privileges)
   - Root User: root (Password: [REDACTED - See Vaultwarden])
   - SSH Key Access: Enabled via standard authorized_keys

4) Network Configuration:
   - Primary LAN IP: 192.168.0.9 (Interface: ens18)
   - Secondary App IP: 10.90.39.104 (Interface: ens20)
   - Tailscale IP: 100.80.103.95
   - Gateway IP: 192.168.0.101 (vmbr0) / 192.168.0.1 (Router)

5) System Go-Live Date:
   - Go-Live Date: 2026-08-07
```

---

### VM 101: `FNT-DEMO` (FNT Command Application Server)

```yaml
1) Software Versions:
   - Operating System: CentOS 7 / RHEL Enterprise Linux
   - Web / Application Server: Apache Tomcat 9.0.x / Apache HTTP Server 2.4
   - Database: Oracle Database 19c Enterprise Edition
   - Remote Management: OpenSSH 7.4, VNC Server (5901)

2) Hardware / Resource Allocation:
   - CPU: 4 vCPUs
   - Memory (RAM): 16.0 GB Total
   - Disk Storage: 80.0 GB Virtual Storage (QEMU disk)

3) Credentials & Access (UID / Password):
   - SSH User: root (Password: [DEMO - fntdemo123])
   - App Admin: fnt (Password: [DEMO - fntdemo123])
   - Oracle DB SID: ORCL / FNTDB (User: system / Password: [DEMO - Password123])

4) Network Configuration:
   - Primary LAN IP: 192.168.0.18 (Bridged)
   - Internal Network IP: 10.90.39.2 (Isolated)
   - Gateway IP: 10.90.39.1 / 192.168.0.101

5) System Go-Live Date:
   - Go-Live Date: 2026-08-07
```

---

### Hypervisor Host: `rm1dev` (Bare-Metal Proxmox Host)

```yaml
1) Software Versions:
   - Hypervisor OS: Proxmox VE 8.2 (Debian 12 Bookworm core)
   - Kernel: 6.8.4-2-pve x86_64
   - Hypervisor Services: QEMU/KVM, LXC, Open vSwitch / Linux Bridges

2) Hardware / Resource Allocation:
   - Hardware: Dell PowerEdge R520 Server
   - CPU: 16 Physical Cores / 32 Threads (Dual Intel Xeon)
   - Memory (RAM): 64.0 GB ECC RAM
   - Storage: 2.0 TB SAS RAID-10 Storage Pool (`/var/lib/vz`)

3) Credentials & Access (UID / Password):
   - Web GUI / SSH User: root
   - Password: [REDACTED - See Vaultwarden]
   - Proxmox Web GUI Port: 8006 (https://192.168.0.101:8006)

4) Network Configuration:
   - Primary Management IP: 192.168.0.101 (vmbr0)
   - Tailscale VPN IP: 100.118.216.78
   - Subnet Routes Advertised: 192.168.0.0/24, 10.90.39.0/24
   - Gateway IP: 192.168.0.1

5) System Go-Live Date:
   - Go-Live Date: 2026-08-04
```

---

## 📦 2. Software & Container Application Inventory

All application services run as Docker containers hosted on **VM 100 (`ubuntu-rm1dev`)**.

| Application Service | Software Image & Version | Access URL / Port | UID / Username | Password / Credentials | Storage & Dependencies | Go-Live Date |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Zammad Helpdesk** | `ghcr.io/zammad/zammad:7.1.2-0000` | `https://zammad.192.168.0.9.nip.io/`<br>`http://192.168.0.9:8084/` | `hafiz@resonantnetworks.com` | `[REDACTED - See Vaultwarden]` | PostgreSQL 17.10, ES 9.4.4, Redis 8.10, Memcached 1.6 | 2026-08-06 |
| **Zabbix Web UI** | `zabbix/zabbix-web-nginx-pgsql:alpine-6.4-latest` | `http://192.168.0.9:8083/` | `Admin` | `zabbix` | PostgreSQL 16 (`zabbix_db`), Nginx | 2026-08-04 |
| **Zabbix Server** | `zabbix/zabbix-server-pgsql:alpine-6.4-latest` | `192.168.0.9:10051` | `zabbix` | `zabbix` | PostgreSQL 16 (`zabbix_db`) | 2026-08-04 |
| **LibreNMS NMS** | `librenms/librenms:latest` | `https://librenms.192.168.0.9.nip.io/`<br>`http://192.168.0.9:8181/` | `root` | `NewPassword@2026` | MariaDB 10 (`Password@123`), Redis 7.2 | 2026-08-04 |
| **Open WebUI (OWUI)** | `ghcr.io/open-webui/open-webui:main` | `https://owui.192.168.0.9.nip.io/`<br>`http://192.168.0.9:8085/` | Admin Account | Configured on first login | SQLite DB, Portainer Bridge | 2026-08-05 |
| **Open Terminal** | `ghcr.io/open-webui/open-terminal:latest` | `http://192.168.0.9:8086/` | Token Auth | System Token | Embedded Terminal Server | 2026-08-05 |
| **Portainer CE** | `portainer/portainer-ce:latest` | `https://192.168.0.9/portainer/`<br>`https://192.168.0.9:9443/` | `admin` | Set on setup (`[REDACTED - See Vaultwarden]`) | Local Docker Socket (`/var/run/docker.sock`) | 2026-08-04 |
| **Vaultwarden** | `vaultwarden/server:latest` | `https://192.168.0.9/vault/`<br>`http://127.0.0.1:8080/` | `hafiz@resonantnetworks.com` | `[REDACTED - See Vaultwarden]` | SQLite Database (`/var/lib/vaultwarden`) | 2026-08-04 |
| **Nginx Reverse Proxy** | `nginx:1.25.5-alpine` (`rm1-zabbix-relay`) | `0.0.0.0:9099` | N/A | N/A | `/etc/nginx/sites-available/reverse-proxy` | 2026-08-04 |
| **Hermes AI Agent** | `nikolaik/python-nodejs:python3.11-nodejs20` | Gateway CLI / Messaging | `ubuntu` | N/A | `/home/ubuntu/.hermes/` | 2026-08-07 |

---

## 🌐 3. Network Architecture & Routing Summary

```
                  ┌──────────────────────────────────────────────┐
                  │ Router / Gateway (192.168.0.1)               │
                  └──────────────────────┬───────────────────────┘
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 │ Proxmox VE Host: rm1dev (192.168.0.101)       │
                 │ Tailscale IP: 100.118.216.78                  │
                 └───────────────┬──────────────────────┬────────┘
                                 │ vmbr0                │ vmbr1
                                 ▼                      ▼
┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────┐
│ VM 100: ubuntu-rm1dev                        │  │ VM 101: FNT-DEMO                    │
│ Primary IP: 192.168.0.9                      │  │ Internal IP: 10.90.39.2             │
│ Secondary IP: 10.90.39.104                   │  │ Bridged IP: 192.168.0.18            │
│ Tailscale IP: 100.80.103.95                  │  │ Role: FNT Command Server            │
│ Role: Docker Host (Zabbix, Zammad, LibreNMS) │  │ Ports: 22, 80, 1521, 5901, 9090     │
└──────────────────────────────────────────────┘  └─────────────────────────────────────┘
```

---

## 🔒 4. Master Credential Directory Quick-Reference

> [!IMPORTANT]
> The following table consolidates all primary system credentials per HQ Directive item (3).

| System / Service Name | Host / IP | Access Port | Username / UID | Password |
| :--- | :--- | :--- | :--- | :--- |
| **Proxmox Hypervisor** | `192.168.0.101` | 8006 (HTTPS) / 22 (SSH) | `root` | `[REDACTED - See Vaultwarden]` |
| **Ubuntu VM (Host SSH)** | `192.168.0.9` | 22 (SSH) | `ubuntu` / `root` | `[REDACTED - See Vaultwarden]` |
| **FNT-DEMO VM (SSH)** | `192.168.0.18` | 22 (SSH) | `root` / `fnt` | `fntdemo123` |
| **Oracle Database** | `10.90.39.2` | 1521 (TCP) | `system` | `Password123` |
| **Zammad Helpdesk** | `zammad.192.168.0.9.nip.io` | 8084 / 443 | `hafiz@resonantnetworks.com` | `[REDACTED - See Vaultwarden]` |
| **Vaultwarden Password Mgr**| `192.168.0.9/vault/` | 8080 / 443 | `hafiz@resonantnetworks.com` | `[REDACTED - See Vaultwarden]` |
| **LibreNMS Web Admin** | `librenms.192.168.0.9.nip.io` | 8181 / 443 | `root` | `NewPassword@2026` |
| **LibreNMS MariaDB** | `localhost` | 3306 (Docker internal) | `librenms` | `Password@123` |
| **Zabbix Web Admin** | `192.168.0.9:8083` | 8083 (HTTP) | `Admin` | `zabbix` |
| **Zabbix Postgres DB** | `localhost` | 5432 (Docker internal) | `zabbix` | `zabbix` |
