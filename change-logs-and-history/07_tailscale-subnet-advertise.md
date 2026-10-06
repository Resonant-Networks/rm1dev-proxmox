# DevOps Log

## 2026-06-25 17:25 — tailscale-subnet-advertise

### Changes
| # | Action | Detail |
|---|--------|--------|
| 1 | **Subnet route** | `sudo tailscale up --advertise-routes=192.168.0.0/24` — advertises local LAN `192.168.0.0/24` to Tailnet |

### Current State
| Node | Tailscale IP | Subnet Routes | Status |
|------|-------------|---------------|--------|
| ubuntu-rm1dev | `100.80.103.95` | `192.168.0.0/24` (approved) | Online |

### Tailnet Peers
| Device | IP | Status |
|--------|----|--------|
| laptop-iecun5n7 (Linux) | `100.91.6.49` | Active |
| laptop-iecun5n7-1 (Windows) | `100.67.205.111` | Active (direct) |
| oppo-reno11-5g | `100.71.231.13` | Online |

### Verification
- `tailscale status` — subnet `192.168.0.0/24` in use
- `tailscale status --json` → `AllowedIPs` includes `192.168.0.0/24`, `PrimaryRoutes` set

### Rollback
```bash
sudo tailscale up --advertise-routes=""
# Then approve removal in Tailscale admin console
```

### Notes
- Subnet route must be approved in Tailscale admin console before traffic flows (already done)
- Other Tailnet peers can reach `192.168.0.x` devices through this node as subnet router
- Tailscale v1.98.4
- **Account:** Currently using personal Google account `hafizmohdrizal@gmail.com` — needs migration to company Google account/email in future
