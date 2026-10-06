# DevOps Log

## 2026-08-04 — Provision Ubuntu VM `ubuntu-rm1dev` into Zabbix

### Changes
| # | Action | Detail |
|---|--------|--------|
| 1 | Installed Zabbix agent2 | `zabbix-agent2` 6.4.21 via Zabbix **Ubuntu noble** repo (`/etc/apt/sources.list.d/zabbix.list`); pinned from default 7.0.x (Ubuntu `universe`) to `1:6.4.21-1+ubuntu24.04` to match 6.4 server |
| 2 | Configured agent | `/etc/zabbix/zabbix_agent2.conf`: `Server=192.168.0.9,172.25.0.0/16`, `ServerActive=192.168.0.9`, `Hostname=ubuntu-rm1dev` |
| 3 | Started agent | `systemctl enable --now zabbix-agent2` → `active (running)`, listening on `10050` |
| 4 | Allowed passing checks | Added docker bridge subnet `172.25.0.0/16` to `Server=` so the server container's passive checks aren't rejected |
| 5 | Created Zabbix host | Via API: host `ubuntu-rm1dev` (hostid `10632`), interface `192.168.0.9:10050`, template `Linux by Zabbix agent` |

### Verification
- `docker exec zabbix-server zabbix_get -s 192.168.0.9 -p 10050 -k "agent.ping"` → `1`
- `... -k "system.hostname"` → `ubuntu-rm1dev`
- `... -k "system.cpu.util[]"` → numeric value
- API host.get: interface `available=1` (green); items showing lastvalues, state `0`

### Rollback
```bash
# Uninstall agent
sudo apt-get remove -y zabbix-agent2
sudo rm -f /etc/apt/sources.list.d/zabbix.list

# Remove host via Zabbix API or web UI (Configuration -> Hosts -> ubuntu-rm1dev)
# API: host.delete hostids=[10632]
```

### Notes
- Agent version pinned to 6.4.21; Ubuntu `resolute` has no Zabbix 6.4 repo (used `noble`).
- Zabbix server docker stack runs on this same VM (192.168.0.9); the server container connects from `172.25.0.0/16`, hence the extra allow-list entry.
- Existing `zabbix-agent` container (host `Zabbix server`) is separate and still active.
