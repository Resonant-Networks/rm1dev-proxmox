# RM1Dev — Proxmox VE Storage Pools Layout

## 1. Storage Overview

Proxmox VE on `rm1dev` utilizes a dual-tier storage architecture separating high-speed I/O workloads (running on the Crucial SSD) from bulk cold storage and backups (running on the 6TB RAID array).

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Proxmox Storage Layout                          │
├────────────────────────────────┬───────────────────────────────────────┤
│ Tier 1: SSD (Crucial 250GB)    │ Tier 2: 6TB RAID Array (/dev/sda2)    │
│ ├─ local      (Directory)      │ └─ storage6tb (Directory)             │
│ │  /var/lib/vz                 │    /mnt/pve/storage6tb                │
│ │  ISOs, Templates, Backups    │    Bulk ISOs, VM Backups, PBS         │
│ └─ local-lvm  (LVM-Thin)       │                                       │
│    data thin-pool (136.5 GB)   │                                       │
│    VM 100 & VM 101 Disks       │                                       │
└────────────────────────────────┴───────────────────────────────────────┘
```

---

## 2. Storage Definitions (`/etc/pve/storage.cfg`)

```ini
dir: local
	path /var/lib/vz
	content import,vztmpl,backup,iso

lvmthin: local-lvm
	thinpool data
	vgname pve
	content images,rootdir

dir: storage6tb
	path /mnt/pve/storage6tb
	content iso,images,vztmpl,backup
```

---

## 3. Storage Pool Capacity & Utilization

| Storage ID | Type | Mount / Path | Total Size | Used | Available | Utilization |
|---|---|---|---|---|---|---|
| **`local`** | Directory | `/var/lib/vz` | 164.5 GB | ~36.7 GB | ~120.5 GB | ~22.3% |
| **`local-lvm`** | LVM-Thin | `pve/data` | 136.5 GB | ~116.3 GB | ~20.1 GB | ~85.2% |
| **`storage6tb`** | Directory | `/mnt/pve/storage6tb` | 5.44 TB | ~88.2 GB | ~5.08 TB | ~1.6% |

---

## 4. Virtual Disk Allocations on `local-lvm`

The `local-lvm` thin pool directly hosts the boot disks for the active virtual machines:

| Virtual Volume | VMID / Guest | Allocated Size | Thin Provisioned | Description |
|---|---|---|---|---|
| `pve-vm--100--disk--0` | VM 100 (`rm1dev-control`) | 4 MB | Yes | EFI Disk / TPM state |
| `pve-vm--100--disk--1` | VM 100 (`rm1dev-control`) | 100 GB | Yes | Ubuntu 24.04 Root OS & Docker |
| `pve-vm--101--disk--1` | VM 101 (`FNT-DEMO`) | 40 GB | Yes | FNT Command Appliance (IDE0) |

---

## 5. Storage Maintenance Runbook

### Checking Pool Health:
```bash
# Proxmox storage status
pvesm status

# Volume group free extents
vgs && pvs

# LVM Thin pool metadata & data percentage
lvs -a -o lv_name,vg_name,lv_size,data_percent,metadata_percent
```

### Expanding LVM-Thin Pool:
If `local-lvm` exceeds 90% utilization:
```bash
lvextend -L +10G /dev/pve/data
```
