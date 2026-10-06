# MOP: Provision a Proxmox Host into Zabbix (Agent)

| | |
|---|---|
| Owner | NOC / Infrastructure |
| Zabbix Server | `192.168.0.9:10051` |
| Template | `Linux by Zabbix agent` |
| Risk | Low – no service disruption to VMs |

## Status
- **DONE** for host `rm1dev` (Proxmox VE) — agent2 installed & active, host `rm1dev` registered.
- Note (2026-08-05): host `10084` was renamed from `Zabbix server` → `rm1dev` (host + agent `Hostname`); docs below use the corrected name.
- See final "Verified on rm1dev" section below.

## Objective
Register a Proxmox VE host into Zabbix and start collecting OS-level metrics (CPU, memory, disk, network) via the Zabbix agent.

## Pre-reqs
- Zabbix server reachable from the Proxmox host (TCP `10051`).
- Root or `sudo` access to the Proxmox shell.
- Note the Proxmox host IP and hostname.

## Procedure

### 1. Install the Zabbix agent on the Proxmox host
> **Important:** Proxmox VE is **Debian-based**, NOT Ubuntu. Do not use the `ubuntu` repo. Check the base first:
> ```bash
> grep VERSION_CODENAME /etc/os-release   # e.g. rm1dev = trixie (Debian 13)
> ```

Add the Zabbix **Debian** repo + signing key. Zabbix 6.4 has no `trixie` dist, so use `bookworm`:
```bash
curl -fsSL https://repo.zabbix.com/zabbix/6.4/debian/gpg \
  | gpg --dearmor -o /usr/share/keyrings/zabbix.gpg
echo "deb [signed-by=/usr/share/keyrings/zabbix.gpg] https://repo.zabbix.com/zabbix/6.4/debian bookworm main" \
  > /etc/apt/sources.list.d/zabbix.list
apt update
apt install -y zabbix-agent2
```

> Use `zabbix-agent2` (agent 2). `zabbix-utils` (provides `zabbix_get`) is **optional** — it is not
> required for monitoring; you can verify from the server side instead (see step 6).

### 2. Configure the agent
Edit `/etc/zabbix/zabbix_agent2.conf`:
```ini
Server=192.168.0.9
ServerActive=192.168.0.9
Hostname=rm1dev
```

> `Hostname` must exactly match the host name later created in the Zabbix UI.

### 3. Start the agent
```bash
systemctl enable --now zabbix-agent2
systemctl restart zabbix-agent2
systemctl status zabbix-agent2 --no-pager
```

### 4. Open the server port (if host firewall enabled)
Proxmox does **not** ship `ufw`. Use `iptables` (or PVE `Datacenter → Firewall → IP tables rules`):
```bash
iptables -I INPUT -p tcp --dport 10050 -j ACCEPT
```
> Active checks are outbound (agent → server `10051`) and need no inbound rule;
> the rule above is only for passive checks (server → agent `10050`).

### 5. Add the host in Zabbix
1. Web UI → **Configuration → Hosts → Create host**.
2. **Host name**: must match `Hostname=` from step 2 (`rm1dev`).
3. **Host groups**: add an appropriate group (e.g. `Proxmox`).
4. **Interfaces → Agent**: IP/DNS = Proxmox host IP, port `10050`.
5. **Templates**: link **"Linux by Zabbix agent"**.
6. Click **Add**, then look for the green host entry.

### 6. Verify
- Host shows **ZBX** (agent) in the status column → data is flowing.
- **Monitoring → Latest data**: select the host and confirm metrics appear.
- Query from the **Zabbix server** (the server image has `zabbix_get`):
  ```bash
  docker exec zabbix-server zabbix_get -s <proxmox-ip> -p 10050 -k "agent.ping"
  docker exec zabbix-server zabbix_get -s <proxmox-ip> -p 10050 -k "system.hostname"
  ```
  (Avoid installing `zabbix_utils` on the Proxmox host — resolves the trixie/bookworm repo issue entirely.)

## Verified on rm1dev (2026-08-04)
- `agent.ping` → `1` and `system.hostname` confirmed via server-side `zabbix_get`.
- Agent2 service: `active (running)`, enabled at boot.
- Config: `Server`/`ServerActive = 192.168.0.9`, `Hostname = rm1dev` (renamed from `Zabbix server` on 2026-08-05; agent2 restarted).
- iptables rule for inbound `10050/tcp` added.

## Rollback
- Remove the host in **Configuration → Hosts**.
- On the Proxmox host: `apt remove -y zabbix-agent2`.

## Notes / Caveats
- This template does **not** cover VM/CT VM-level metrics. For Proxmox API metrics (VM CPU, disk, QoS) use the community `pve` API templates.
- Keep the agent version in line with the Zabbix server version (6.4).