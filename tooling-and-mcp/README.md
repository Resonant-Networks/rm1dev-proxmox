# Proxmox Model Context Protocol (MCP) Server Tooling

## 1. Overview

This directory contains MCP server implementations enabling AI agents (Antigravity, Opencode, Claude Desktop) to interact directly with the Proxmox VE REST API on `rm1dev` (`https://192.168.0.101:8006`).

---

## 2. Server Scripts

* **`proxmox_mcp_stdio.py`**: Standard Input/Output (stdio) transport MCP server. Used by local CLI assistants and editor extensions.
* **`proxmox_mcp_sse.py`**: Server-Sent Events (SSE) HTTP transport MCP server for network-accessible agent integration.

---

## 3. Supported MCP Capabilities

| Tool Name | Description |
|---|---|
| `list_nodes` | Enumerate all cluster nodes and health status |
| `list_vms` | List all QEMU virtual machines on `rm1dev` |
| `list_lxc_containers` | List all LXC containers |
| `get_instance_config` | Fetch VM / container hardware and network configuration |
| `power_control` | Start, stop, shutdown, reset, or suspend VM/LXC |
| `list_storage` | Enumerate active storage pools (`local`, `local-lvm`, `storage6tb`) |
| `list_storage_content` | Query ISOs, disk images, and backups in a storage pool |
| `create_snapshot` | Take point-in-time VM/LXC snapshots prior to maintenance |
| `rollback_snapshot` | Revert instance state to a previous snapshot |
| `delete_instance` | Destroy VM or container |
| `get_resource_usage` | Fetch real-time CPU, RAM, and disk metrics |

---

## 4. MCP Server Configuration

Example configuration stanza for `settings.json` or `opencode.jsonc`:

```json
{
  "mcpServers": {
    "proxmox": {
      "command": "python3",
      "args": ["/path/to/rm1dev-proxmox/tooling-and-mcp/proxmox_mcp_stdio.py"],
      "env": {
        "PROXMOX_HOST": "192.168.0.101",
        "PROXMOX_PORT": "8006",
        "PROXMOX_USER": "root@pam",
        "PROXMOX_VERIFY_SSL": "false"
      }
    }
  }
}
```
