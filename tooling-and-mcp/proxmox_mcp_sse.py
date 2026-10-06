#!/usr/bin/env python3
import os
import sys
from proxmox_mcp.server import mcp
from mcp.server.transport_security import TransportSecuritySettings

# Load Proxmox credentials
os.environ["PROXMOX_URL"] = os.getenv("PROXMOX_URL", "https://192.168.0.101:8006")
os.environ["PROXMOX_TOKEN_NAME"] = os.getenv("PROXMOX_TOKEN_NAME", "root@pam!mcp")
os.environ["PROXMOX_TOKEN_VALUE"] = os.getenv("PROXMOX_TOKEN_VALUE", "88412900-8226-4a7f-acbb-0c2ef51473c1")
os.environ["PROXMOX_VERIFY_SSL"] = os.getenv("PROXMOX_VERIFY_SSL", "false")

def main():
    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = 8095
    mcp.settings.transport_security = TransportSecuritySettings(
        enable_dns_rebinding_protection=False,
        allowed_hosts=["*"],
        allowed_origins=["*"]
    )
    print("Starting Proxmox MCP SSE Server on http://0.0.0.0:8095/sse ...")
    mcp.run(transport="sse")

if __name__ == "__main__":
    main()
