# DevOps Log

## 2026-06-25 05:12 — initial-system-setup

### Changes
| # | Action | Detail |
|---|--------|--------|
| 1 | **Tailscale** | Installed via `curl -fsSL https://tailscale.com/install.sh \| sh`, authenticated, node name `ubuntu-rm1dev`, IP `100.80.103.95` |
| 2 | **Docker CE** | Installed official Docker CE (docker-ce, docker-ce-cli, containerd.io, buildx, compose-plugin). User `ubuntu` added to `docker` group. |
| 3 | **Portainer volume** | Created `portainer_data` Docker volume |
| 4 | **nginx** | Installed `nginx 1.28.3`, enabled via systemd, `ufw allow 'Nginx Full'` |
| 5 | **nmap** | Installed `nmap` via apt |
| 6 | **Basic net-tools** | Installed `bridge-utils`, `iproute2`, `net-tools` |

### Verification
- `tailscale status` → `ubuntu-rm1dev` connected, IP `100.80.103.95`
- `docker --version` → Docker CE
- `nginx -v` → `nginx/1.28.3`
- `sudo ufw status` → Nginx Full allowed

### Rollback
```bash
# Remove Tailscale
sudo tailscale down && sudo apt remove --purge tailscale -y

# Remove Docker CE
sudo apt remove --purge docker-ce docker-ce-cli containerd.io -y
sudo rm -rf /var/lib/docker

# Remove nginx
sudo apt remove --purge nginx nginx-common -y
sudo rm -rf /etc/nginx

# Remove extra packages
sudo apt remove --purge nmap bridge-utils net-tools -y
```

### Notes
- All installs used official repos (Docker from download.docker.com, nginx from Ubuntu repos)
- No Docker Compose files were created yet; everything was ad-hoc `docker run`
