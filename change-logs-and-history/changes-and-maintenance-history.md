# RM1Dev — Hypervisor Modification & Maintenance History

This document provides a chronological record of all structural modifications, network adaptations, storage realignments, and guest provisioning activities performed on the **`rm1dev`** Proxmox host.

---

## 📅 Timeline of Key Infrastructure Milestones

### 1. Bare-Metal Deployment & Base Proxmox Installation
* **Date:** June 2026
* **Host:** Dell PowerEdge R520 (Service Tag `J3FSWX1`)
* **Actions:**
  - Deployed Proxmox VE via Virtual Media using HTML5 console.
  - Initialized OS root on Crucial MX500 250GB SSD (`/dev/sdb`).
  - Configured management bridge `vmbr0` on `nic0` (`192.168.0.101/24`).

---

### 2. Tailscale Subnet Router & Kernel Forwarding
* **Date:** June 25, 2026
* **Actions:**
  - Installed Tailscale on Proxmox host (`100.118.216.78`).
  - Enabled `net.ipv4.ip_forward = 1` and `net.ipv6.conf.all.forwarding = 1` in kernel sysctl.
  - Advertised subnets: `192.168.0.0/24` (LAN) and `10.90.39.0/24` (Isolated bridge).
  - Approved advertised routes in Tailscale admin console.

---

### 3. Isolated Application Bridge (`vmbr1`) & DHCP Setup
* **Date:** June 25, 2026
* **Actions:**
  - Configured Linux bridge `vmbr1` with IP `10.90.39.1/24` for VM isolation.
  - Installed and configured `dnsmasq` on Proxmox to provide static DHCP leases on `vmbr1`:
    - `10.90.39.2` for VM 101 (`FNT-DEMO`).
    - `10.90.39.104` for VM 100 secondary interface.

---

### 4. FNT Command Appliance Import & Storage Fixes
* **Date:** June 25, 2026
* **Actions:**
  - Transferred 14GB VMDK appliance to Proxmox.
  - Used `qm importdisk` to import disk into `local-lvm`.
  - Discovered initramfs AHCI driver incompatibility when attached via SATA.
  - Resolved boot failure by switching bus to **IDE** (`ide0`), matching the original OVF specification.
  - Configured static DHCP lease and host routing.

---

### 5. 6TB PERC H710 RAID Volume Allocation & PBS Setup
* **Date:** September 2026
* **Actions:**
  - Removed unused raw LVM definition `data2`.
  - Partitioned `/dev/sda` with GPT and formatted `/dev/sda2` as `ext4` with label `storage6tb`.
  - Created mount directory `/mnt/pve/storage6tb` and added persistent `/etc/fstab` entry.
  - Added `storage6tb` directory storage in Proxmox VE storage configuration (`/etc/pve/storage.cfg`) for ISOs, templates, and VM backups.

---

### 6. Monitoring Integration (Zabbix Agent 2)
* **Date:** August 2026
* **Actions:**
  - Installed `zabbix-agent2` on Proxmox host.
  - Configured active and passive monitoring pointed at Zabbix Server (`192.168.0.9:10051`).
  - Successfully registered host `rm1dev` with the `Linux by Zabbix agent` template.
