# Standard Operating Procedure (SOP): Proxmox VE Installation via Virtual Media

| Document Property | Value |
|---|---|
| **Document Version** | 1.0 |
| **Target OS** | Proxmox VE 8.x / 9.x |
| **Deployment Method** | Remote Bare-Metal via Out-of-Band (OOB) Virtual Media (iDRAC / iLO / IPMI) |
| **Target Host** | Dell PowerEdge R520 (`rm1dev`) |
| **Author** | Resonant Networks Infrastructure Team |

---

## 1. Scope & Objective

This Standard Operating Procedure (SOP) details the steps required to perform a bare-metal installation of Proxmox Virtual Environment (PVE) on a remote server using the **Virtual Media** mounting method. This method completely eliminates the need for physical USB drives or on-site datacenter technician access.

---

## 2. Prerequisites & Preparation

| Prerequisite Item | Details & Source |
|---|---|
| **Proxmox VE ISO Image** | Official ISO downloaded from [https://www.proxmox.com/en/downloads](https://www.proxmox.com/en/downloads) |
| **Out-of-Band (OOB) Access** | IP connectivity and administrator credentials to iDRAC / ZPE Nodegrid / BMC |
| **Client Workstation** | Browser with HTML5 Virtual Console support (Chrome / Firefox / Edge) |
| **Network Allocation** | Static Management IP (`192.168.0.101/24`), Gateway (`192.168.0.1`), DNS (`192.168.0.1`), FQDN (`rm1dev.resonantnetworks.local`) |
| **Storage Controller** | Hardware RAID array configured on Dell PERC H710 or raw SSD target |

---

## 3. Out-of-Band Virtual Media Mounting

### 3.1 Step 1: Connect to Server Out-of-Band Management
1. Navigate to the OOB management IP in your browser.
2. Authenticate using administrative credentials.
3. Launch the **HTML5 Virtual Console**.

### 3.2 Step 2: Mount the Proxmox ISO Image
Depending on the remote management subsystem:

| Vendor BMC System | Virtual Media Menu Location | Mounting Action |
|---|---|---|
| **Dell PowerEdge (iDRAC 7/8/9)** | `Virtual Media` → `Map CD/DVD` | Browse to local `proxmox-ve_*.iso` and click **Map Device** |
| **HPE ProLiant (iLO 5/6)** | `Virtual Media` → `Disc Image File` | Select ISO and enable Scripted Media |
| **Supermicro (IPMI / BMC)** | `Virtual Media` → `CD-ROM Image` | Share ISO via HTTP/SAMBA or local HTML5 mount |
| **Cisco UCS (IMC)** | `Virtual Media` → `Map CD/DVD` | Select ISO and click Mount Drive |

> [!IMPORTANT]
> **Network Stability Notice:** Ensure your workstation maintains an uninterrupted connection to the BMC interface throughout installation. The server streams packages remotely through your client session during installation.

---

## 4. One-Time Boot Selection & ISO Boot

1. Power on or hard-reset the physical server from the Virtual Console power control menu.
2. Watch the BIOS POST screen and press the **One-Time Boot Menu** key:
   * **Dell PowerEdge:** Press **F11** for Boot Manager.
   * **HPE ProLiant:** Press **F11** for One-Time Boot Menu.
   * **Supermicro:** Press **F11** or **F12** for Boot Device Menu.
3. Select **Virtual CD/DVD-ROM** or **Virtual Optical Drive** from the boot device list.
4. Press `<Enter>` to boot into the Proxmox VE Installer.

---

## 5. Proxmox VE Graphical Installation Steps

### 5.1 Welcome & License Agreement
Select **Install Proxmox VE (Graphical)**. Review and accept the End User License Agreement (EULA).

### 5.2 Target Harddisk Selection & Filesystem
Select the target boot drive. Click **Options** to select the target filesystem:

| Filesystem Option | Recommended Use Case | Configuration Notes |
|---|---|---|
| **ext4** | Single SSD or Hardware RAID Controller | Standard Linux filesystem when PERC H710 presents virtual drives |
| **zfs (RAID1)** | Dual Enterprise NVMe / SATA SSDs | Redundant mirrored boot pool with software checksumming |
| **zfs (RAID10)** | 4+ NVMe / SATA Disks | High performance & fault tolerance |

*For `rm1dev`: Select the 250GB Crucial SSD (`/dev/sdb`) with `ext4`.*

### 5.3 Regional & Localization Settings
* **Country:** Singapore / Malaysia / United States
* **Timezone:** Selected datacenter timezone (e.g. `Asia/Kuala_Lumpur` or `Asia/Singapore`)
* **Keyboard Layout:** US English

### 5.4 Administrator Password & Alert Email
Specify the root password and enter the technical alert contact email address.

### 5.5 Management Network Configuration
Configure the primary network interface dedicated to hypervisor management:

| Parameter | Configuration Value (`rm1dev`) | Description |
|---|---|---|
| **Management Interface** | `nic0` (`enp2s0f0`) | Primary physical onboard gigabit NIC |
| **Hostname (FQDN)** | `rm1dev` | Hypervisor node name |
| **IP Address (CIDR)** | `192.168.0.101/24` | Static management IP assigned to `vmbr0` |
| **Default Gateway** | `192.168.0.1` | Local network router gateway |
| **DNS Server** | `192.168.0.1` / `8.8.8.8` | Primary domain name server |

### 5.6 Summary & Installation Execution
Review settings on the summary page. Click **Install**.

---

## 6. Post-Installation & Virtual Media Cleanup

1. When installation completes (100%), unmount/unmap the ISO from the Virtual Media menu.
2. Reboot the server.
3. Connect to the Proxmox Web Management GUI:
   👉 **`https://192.168.0.101:8006/`**
4. Log in with Realm: `Linux PAM`, Username: `root`.

---

## 7. Post-Install Host Hardening & Verification

Run these post-installation commands in the host shell:

```bash
# 1. Disable enterprise repository and enable pve-no-subscription repository
cat <<EOF > /etc/apt/sources.list.d/pve-enterprise.list
# deb https://enterprise.proxmox.com/debian/pve trixie pve-enterprise
deb http://download.proxmox.com/debian/pve trixie pve-no-subscription
EOF

# 2. Update packages to latest stable releases
apt update && apt dist-upgrade -y

# 3. Verify storage pools
pvesm status

# 4. Verify network bridges
ip link show vmbr0
```
