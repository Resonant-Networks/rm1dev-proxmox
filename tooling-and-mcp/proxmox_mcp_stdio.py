#!/usr/bin/env python3
import os
import sys
from proxmox_mcp.server import mcp

# Load Proxmox credentials
os.environ["PROXMOX_URL"] = os.getenv("PROXMOX_URL", "https://192.168.0.101:8006/api2/json")
os.environ["PROXMOX_TOKEN_NAME"] = os.getenv("PROXMOX_TOKEN_NAME", "root@pam!mcp")
os.environ["PROXMOX_TOKEN_VALUE"] = os.getenv("PROXMOX_TOKEN_VALUE", "88412900-8226-4a7f-acbb-0c2ef51473c1")
os.environ["PROXMOX_VERIFY_SSL"] = os.getenv("PROXMOX_VERIFY_SSL", "false")

def main():
    mcp.run()

if __name__ == "__main__":
    main()
