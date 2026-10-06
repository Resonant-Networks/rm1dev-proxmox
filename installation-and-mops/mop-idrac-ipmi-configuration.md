# Method of Procedure (MOP): Dell iDRAC / BMC IPMI Static IP Configuration

| Property | Value |
|---|---|
| **Host** | `rm1dev` (Dell PowerEdge R520) |
| **Tool** | `ipmitool` (OpenIPMI Linux Driver) |
| **Channel** | LAN Channel 1 (`lan 1`) |
| **Target Static IP** | `169.254.0.100 / 16` |

---

## 1. Overview

This MOP provides the commands to configure static IP addressing on the Dell Baseboard Management Controller (BMC / iDRAC) directly from the running Proxmox host operating system using the kernel IPMI driver.

---

## 2. Configuration Procedure

Execute the following commands as `root` on `rm1dev`:

```bash
# 1. Set LAN Channel 1 IP addressing mode to static
ipmitool lan set 1 ipsrc static

# 2. Assign static IP address
ipmitool lan set 1 ipaddr 169.254.0.100

# 3. Set subnet mask
ipmitool lan set 1 netmask 255.255.0.0

# 4. Set default gateway IP (0.0.0.0 for direct link / link-local)
ipmitool lan set 1 defgw ipaddr 0.0.0.0
```

---

## 3. Verification

Verify the applied network parameters on LAN Channel 1:

```bash
ipmitool lan print 1
```

Expected output includes:
```text
IP Address Source       : Static Address
IP Address              : 169.254.0.100
Subnet Mask             : 255.255.0.0
Default Gateway IP      : 0.0.0.0
```
