# Enterprise Production Plan: 6TB Storage & Proxmox Backup Server (PBS) Setup

**Target Host:** `rm1dev` (Proxmox VE 9.2.11 / `192.168.0.101`)  
**Target Drive:** `/dev/sda` (6TB DELL PERC H710 RAID Volume)  
**Goal:** Convert unused raw LVM `data2` into a high-performance, deduplicated Proxmox Backup Server (PBS) datastore to handle all VM/LXC backups and free up the overflowing 250GB SSD.

---

## Current vs. Target Architecture

```
[ Current State ]
- SSD (250GB): local (94% FULL) + local-lvm (Holds all VMs: 100, 101, 200, 201)
- 6TB HDD (sda): data2 (Raw LVM - Empty, but restricted to VM disks only; CANNOT take backups)

[ Target Enterprise State ]
- SSD (250GB): Host OS + High-IOPS VM Virtual Disks (local-lvm)
- 6TB HDD (sda): Formatted ext4 mounted at /mnt/pve/storage6tb
                 └── PBS Datastore (Deduplicated, Incremental Backups + ISO Storage)
```

---

## Phase 1: Convert `/dev/sda` (`data2`) into a Mounted Filesystem

Run these commands on host `rm1dev` as `root` (via SSH or Proxmox Host Shell):

```bash
# 1. Remove the empty LVM storage definition from Proxmox VE
pvesm remove data2

# 2. Remove the empty Volume Group and Physical Volume
vgremove -y data2
pvremove -y /dev/sda

# 3. Create a fresh GPT partition table and ext4 filesystem on /dev/sda
parted -s /dev/sda mklabel gpt
parted -s /dev/sda mkpart primary ext4 0% 100%
mkfs.ext4 -F -L storage6tb /dev/sda1

# 4. Create the mount directory and mount the 6TB volume
mkdir -p /mnt/pve/storage6tb
mount /dev/sda1 /mnt/pve/storage6tb

# 5. Add to /etc/fstab for automatic persistence across reboots
echo "LABEL=storage6tb /mnt/pve/storage6tb ext4 defaults,nofail 0 2" >> /etc/fstab
```

---

## Phase 2: Install Proxmox Backup Server (PBS)

On Proxmox VE, PBS can be installed directly alongside PVE on the host or inside an LXC container. **Installing natively on host `rm1dev`** is recommended for maximum disk throughput and zero virtualization overhead.

```bash
# 1. Update package list and install Proxmox Backup Server packages
apt update
apt install -y proxmox-backup-server

# 2. Create the PBS datastore directory on the 6TB disk
mkdir -p /mnt/pve/storage6tb/pbs-datastore
chown -R backup:backup /mnt/pve/storage6tb/pbs-datastore

# 3. Initialize the PBS Datastore
proxmox-backup-manager datastore create Backup6TB /mnt/pve/storage6tb/pbs-datastore
```

---

## Phase 3: Connect PBS Datastore to Proxmox VE

1. Open **Proxmox VE GUI** (`https://192.168.0.101:8006`).
2. Navigate to **Datacenter** $\rightarrow$ **Storage** $\rightarrow$ **Add** $\rightarrow$ **Proxmox Backup Server**.
3. Fill in the configuration:
   * **ID:** `PBS-6TB`
   * **Server:** `localhost` (or `127.0.0.1`)
   * **User:** `root@pam`
   * **Datastore:** `Backup6TB`
   * **Fingerprint:** *(Optional for localhost; check via `proxmox-backup-manager cert info` if prompted)*
4. Click **Add**.

---

## Phase 4: Configure Enterprise Backup & Prune Schedule

1. Go to **Datacenter** $\rightarrow$ **Backup** $\rightarrow$ Click **Add**.
   * **Node:** `rm1dev`
   * **Storage:** `PBS-6TB`
   * **Schedule:** `02:00` (Every night at 2:00 AM)
   * **Selection Mode:** `All VMs` (Includes VM 100 `rm1dev-control`, VM 101, VM 200, VM 201)
   * **Mode:** `Snapshot`
2. Configure **Prune / Retention Rules** under PBS Datastore settings:
   * **Keep Daily:** `7`
   * **Keep Weekly:** `4`
   * **Keep Monthly:** `12`
   * **Keep Yearly:** `1`

---

## Phase 5: (Optional) Also Add 6TB Directory for ISOs & Large Disks

To store ISO installers and extra template files directly on the 6TB drive without filling up your SSD:

```bash
mkdir -p /mnt/pve/storage6tb/iso-storage
```

In Proxmox Web GUI:
* **Datacenter** $\rightarrow$ **Storage** $\rightarrow$ **Add** $\rightarrow$ **Directory**.
* **ID:** `ISO-6TB`
* **Directory:** `/mnt/pve/storage6tb/iso-storage`
* **Content:** `ISO image`, `Container template`

---

## Verification Checklist

- [ ] `/mnt/pve/storage6tb` is mounted and showing ~5.8 TiB available via `df -h`.
- [ ] PBS Web UI accessible at `https://192.168.0.101:8007`.
- [ ] `PBS-6TB` storage appears under PVE Datacenter Storage list with a green checkmark.
- [ ] Test backup initiated for VM 100 (`rm1dev-control`) finishes cleanly with deduplication enabled.
