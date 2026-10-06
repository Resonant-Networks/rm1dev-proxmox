# RM1Dev — RAID Controller & Disk Configuration

## 1. RAID Controller Architecture

The Dell PowerEdge R520 host (`rm1dev`) is equipped with a hardware SAS RAID controller:

| Property | Value |
|---|---|
| **Controller Model** | **Dell PERC H710 Mini (Integrated)** |
| **PCI Identifier** | `01:00.0 RAID bus controller: Broadcom / LSI MegaRAID SAS 2208 [Thunderbolt] (rev 05)` |
| **Cache Memory** | 512 MB Non-Volatile Battery-Backed Write Cache (BBU) |
| **Interface Speed** | 6 Gb/s SAS / SATA per port |
| **RAID Levels Supported** | RAID 0, 1, 5, 6, 10, 50, 60 |
| **Operating Mode** | Hardware RAID Virtual Drive Presentation |

---

## 2. Logical Disks (Virtual Drives) Presented to Proxmox

The operating system detects two physical block devices:

```
Device     Size     Type    Hardware Source              Mount / Usage
/dev/sda   5.5 TB   HDD     PERC H710 SAS Virtual Drive  sda1: 100GB (pve-root LVM)
                                                         sda2: 5.4TB (/mnt/pve/storage6tb ext4)
/dev/sdb   250 GB   SSD     Crucial MX500 SATA SSD       sdb1: BIOS Boot
                                                         sdb2: /boot/efi (1GB vfat)
                                                         sdb3: LVM Physical Volume (pve VG)
```

---

## 3. Physical Drive Inventory Behind RAID Controller

Direct inspection via MegaRAID passthrough (`smartctl -d megaraid,N /dev/sda`) identifies the physical drives installed in the server hot-swap bays:

### Physical Drive Bay 0:
* **Vendor & Model**: Toshiba `MG04SCA40EN`
* **Serial Number**: `1760A00TFVNC`
* **User Capacity**: 4.0 TB [4,000,787,030,016 bytes]
* **Rotation Rate**: 7,200 RPM
* **Transport**: SAS 6 Gb/s (SPL-4)
* **Status**: SMART Health OK

### Physical Drive Bay 1:
* **Vendor & Model**: Toshiba `MG03SCA300`
* **Serial Number**: `Y370A05KFVL9`
* **User Capacity**: 3.0 TB [3,000,592,982,016 bytes]
* **Rotation Rate**: 7,200 RPM
* **Transport**: SAS 6 Gb/s (SPL-4)
* **Status**: SMART Health OK

### Physical Drive Bay 2:
* **Vendor & Model**: Toshiba `MG03SCA300`
* **Serial Number**: `Y370A0NJFVL9`
* **User Capacity**: 3.0 TB [3,000,592,982,016 bytes]
* **Rotation Rate**: 7,200 RPM
* **Transport**: SAS 6 Gb/s (SPL-4)
* **Status**: SMART Health OK

---

## 4. Solid-State Drive (SSD) Configuration

* **Model**: Crucial / Micron `CT250MX500SSD1` (MX500 2.5" SATA SSD)
* **Serial Number**: `2118E59C86E7`
* **Capacity**: 250 GB [250,059,350,016 bytes]
* **Firmware**: `M3CR023`
* **Interface**: SATA 3.3 (6.0 Gb/s link)
* **Role**: Primary operating system boot disk and high-performance LVM-Thin storage pool (`local-lvm`) hosting VM system disks.

---

## 5. SMART Diagnostics & Monitoring Syntax

Because `/dev/sda` is managed by an LSI MegaRAID controller, standard `smartctl -a /dev/sda` will return an error requesting controller flags. Use the following syntax to query physical drives:

```bash
# Query Drive in Slot 0
smartctl -d megaraid,0 -a /dev/sda

# Query Drive in Slot 1
smartctl -d megaraid,1 -a /dev/sda

# Query Drive in Slot 2
smartctl -d megaraid,2 -a /dev/sda

# Query Crucial SSD directly
smartctl -a /dev/sdb
```
