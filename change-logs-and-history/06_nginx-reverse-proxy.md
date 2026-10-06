# DevOps Log

## 2026-06-25 17:02 — nginx-reverse-proxy

### Changes
| # | Action | Detail |
|---|--------|--------|
| 1 | **SSL cert** | Generated self-signed wildcard cert `/etc/nginx/ssl/selfsigned.{crt,key}` (RSA 2048, 10yr, SAN: ubuntu-rm1dev, localhost, 192.168.0.9) |
| 2 | **nginx config** | Created `/etc/nginx/sites-available/reverse-proxy` replacing default |
| 3 | **HTTP→HTTPS** | Port 80 redirects all traffic to HTTPS (301) |
| 4 | **Path routing** | `/portainer/` → `https://127.0.0.1:9443` |
| 5 | **WebSocket** | Upgrade headers set for upstream |
| 6 | **Portainer base-url** | Recreated container with `--base-url /portainer` for subpath support |

### Verification
- HTTP→HTTPS redirect: `curl -I http://localhost` → `301 Moved Permanently` ✓
- Portainer: `curl -sk https://localhost/portainer/` → returns Portainer login page ✓
- nginx config: `nginx -t` → syntax ok ✓

### Rollback
```bash
# Restore default nginx
sudo rm /etc/nginx/sites-enabled/reverse-proxy
sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/
sudo systemctl reload nginx

# Remove self-signed cert
sudo rm -rf /etc/nginx/ssl

# Restore Portainer without base-url
docker stop portainer && docker rm portainer
docker run -d --name portainer --restart always \
  -p 8000:8000 -p 9443:9443 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest
```

## 2026-06-25 17:45 — vaultwarden-nginx-fix

### Changes
| # | Action | Detail |
|---|--------|--------|
| 1 | **nginx** | Added `location /vault/` block proxying to `http://127.0.0.1:8080` |
| 2 | **Fix** | Removed trailing slash from `proxy_pass` — Vaultwarden 1.36.0 handles subpath internally via `DOMAIN` env var, so prefix must not be stripped |

### Verification
- `curl -sk https://localhost/vault/` → Vaultwarden Web UI ✓
- `curl -sk https://localhost/portainer/` → still OK ✓
- nginx: `nginx -t` → syntax ok ✓

## Current State (2026-06-25)

### Running Config
| Route | Upstream | Trailing slash? | Notes |
|-------|----------|----------------|-------|
| `/portainer/` | `https://127.0.0.1:9443/` | Yes (strips prefix) | Portainer also accessible directly on `0.0.0.0:9443` |
| `/vault/` | `http://127.0.0.1:8080` | No (passes prefix) | Vaultwarden handles subpath internally |
| `/` | — | — | Returns 404 |

### Tailnet Access
Tailscale devices on `tail102e60.ts.net` reach services behind nginx via:

**Recommended (via nginx, all HTTPS):**
| Method | URL | Notes |
|--------|-----|-------|
| Magic DNS | `https://ubuntu-rm1dev.tail102e60.ts.net/vault/` | Tailscale DNS, works anywhere on tailnet |
| Magic DNS | `https://ubuntu-rm1dev.tail102e60.ts.net/portainer/` | Same |
| Tailscale IP | `https://100.80.103.95/vault/` | Works even if DNS is flaky |

**Direct (bypasses nginx):**
| Service | URL | Notes |
|---------|-----|-------|
| Portainer | `https://ubuntu-rm1dev.tail102e60.ts.net:9443` | Binds `0.0.0.0:9443` — accessible from any tailnet device directly |

All SSL is self-signed. Browsers will show a warning — proceed past it.

### Vaultwarden Rollback
```bash
# Remove nginx vaultwarden location block
sudo nano /etc/nginx/sites-available/reverse-proxy  # delete location /vault/ block
sudo nginx -t && sudo systemctl reload nginx

# Stop and remove vaultwarden (including volume data)
docker compose -f /home/ubuntu/vaultwarden/docker-compose.yml down -v
rm -rf /home/ubuntu/vaultwarden
```

### Notes
- Self-signed cert → browser security warning (expected for internal Tailnet use)
- Portainer `0.0.0.0:9443` binds all interfaces — accessible directly from tailnet, bypassing nginx
- Vaultwarden binds `127.0.0.1:8080` only — must go through nginx or from localhost
- Portainer rollback (in section 1) is stale: recreates without `--base-url /portainer` and without `127.0.0.1` binding; if rolled back, update the `docker run` to match current config
- When adding new services: append `location` block, bind upstream to `127.0.0.1` for security
- clab-api-server Exited(137) — not proxied through nginx
