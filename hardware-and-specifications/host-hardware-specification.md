# RM1Dev — Bare-Metal Hardware Specification

## 1. System Identity & Chassis

| Property | Value |
|---|---|
| **Hostname** | `rm1dev` |
| **System Manufacturer** | Dell Inc. |
| **Product Name** | PowerEdge R520 |
| **Form Factor** | 2U Rackmount Server |
| **Service Tag** | `J3FSWX1` |
| **Environment / Site** | RM1 Lab, Resonant Networks |
| **Hypervisor OS** | Proxmox Virtual Environment 9.2 (Debian 13 Trixie core) |
| **Kernel** | Linux 7.0.14-15-pve (x86_64, UEFI Boot Mode) |

---

## 2. Processor Topology (CPU)

| Property | Specification |
|---|---|
| **Processor Model** | Intel(R) Xeon(R) CPU E5-2470 v2 |
| **Processor Architecture** | Ivy Bridge-EN (22 nm) |
| **Base Clock Frequency** | 2.40 GHz (Turbo up to 3.20 GHz) |
| **Physical Sockets** | 2 Sockets populated |
| **Physical Cores** | 20 Cores (10 cores per socket) |
| **Logical Threads (vCPUs)** | 40 Threads (Hyper-Threading enabled) |
| **L3 Cache** | 25 MB Intel Smart Cache per socket (50 MB Total) |
| **Virtualization Extensions** | Intel VT-x, VT-d, EPT enabled |

---

## 3. System Memory (RAM)

| Property | Specification |
|---|---|
| **Total Physical RAM** | 128 GB Registered ECC DDR3 (125.8 GB usable) |
| **Memory Speed** | 1600 MT/s |
| **Swap Space** | 8.0 GB LVM partition (`/dev/pve/swap`) |
| **Memory Allocation** | ~50 GB assigned to VM 100 (`rm1dev-control`), 16 GB to VM 101 (`FNT-DEMO`), remaining reserved for host and dynamic workloads |

---

## 4. Storage Controllers & Drive Architecture

| Component | Hardware Specification |
|---|---|
| **RAID Controller** | Broadcom / LSI MegaRAID SAS 2208 [Thunderbolt] (rev 05) — **Dell PERC H710 Mini** |
| **RAID Cache** | 512 MB NV Non-Volatile Battery-Backed Write Cache |
| **Array Drive (`/dev/sda`)** | 6.0 TB Logical Volume (5.5 TB usable) formatted with GPT |
| **Solid-State Drive (`/dev/sdb`)** | 250 GB Crucial MX500 SATA SSD (`CT250MX500SSD1`, Serial: `2118E59C86E7`) |
| **Physical SAS Drives** | Toshiba Enterprise SAS 7200 RPM (e.g. `MG04SCA40EN` 4TB, `MG03SCA300` 3TB) |

---

## 5. Network Interface Controllers (NICs)

| Interface | Device / Chipset | MAC Address | Operating Role |
|---|---|---|---|
| **`nic0`** | Broadcom NetXtreme BCM5720 GbE (`enp2s0f0`) | `90:b1:1c:55:3e:da` | Uplink port connected to `vmbr0` (Management LAN `192.168.0.101/24`) |
| **`nic1`** | Broadcom NetXtreme BCM5720 GbE (`enp2s0f1`) | `90:b1:1c:55:3e:db` | Dedicated Network Element interface (`10.10.10.1/24`) |
| **`nic2`** | Secondary Gigabit Controller (`enxa0369f157dc0`) | `a0:36:9f:15:7d:c0` | Standby / Lab interface (Down) |
| **`nic3`** | Secondary Gigabit Controller (`enxa0369f157dc1`) | `a0:36:9f:15:7d:c1` | Standby / Lab interface (Down) |

---

## 6. Remote Management & Out-of-Band (OOB)

| Interface | Address / Endpoint | Access Method |
|---|---|---|
| **Proxmox Web UI** | `https://192.168.0.101:8006/` | Port 8006, HTTPS |
| **Tailscale Subnet IP** | `https://100.118.216.78:8006/` | Tailscale Mesh VPN |
| **ZPE Nodegrid (OOB)** | `192.168.0.17` (COM2 Serial) | Serial console `console com2` / Web UI |
| **Internal BMC / iDRAC** | `169.254.0.100` | Static IPMI Lan Channel 1 |
