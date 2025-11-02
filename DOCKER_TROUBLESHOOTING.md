# Docker Network Troubleshooting Guide

## Current Issue
Docker cannot pull images due to DNS resolution failure for Cloudflare storage domains. This is common on university/corporate networks.

## Quick Solutions (Try in order)

### Solution 1: Change Docker Desktop DNS Settings

1. Open **Docker Desktop**
2. Click the **Settings** (gear icon)
3. Go to **Resources** → **Network**
4. Under **DNS Server**, change from "Automatic" to manual DNS servers:
   - Primary: `8.8.8.8` (Google DNS)
   - Secondary: `8.8.4.4` (Google DNS backup)
   - OR use Cloudflare DNS: `1.1.1.1` and `1.0.0.1`
5. Click **Apply & Restart**

### Solution 2: Change System DNS (Windows)

1. Open **Network Settings** → **Change adapter options**
2. Right-click your active network adapter → **Properties**
3. Select **Internet Protocol Version 4 (TCP/IPv4)** → **Properties**
4. Select **Use the following DNS server addresses**:
   - Preferred: `8.8.8.8`
   - Alternate: `8.8.4.4`
5. Click **OK** and restart Docker Desktop

### Solution 3: Configure Docker Daemon DNS

Create or edit `C:\Users\<YourUsername>\.docker\daemon.json`:

```json
{
  "dns": ["8.8.8.8", "8.8.4.4"]
}
```

Then restart Docker Desktop.

### Solution 4: Use VPN or Different Network

If you're on a restricted university network:
- Try connecting via VPN (if available)
- Try using mobile hotspot temporarily
- Check if your university has Docker Hub whitelist requirements

### Solution 5: Test Connection

After applying DNS changes, test:
```powershell
# Test DNS resolution
nslookup docker-images-prod.6aa30f8b08e16409b46e0173d6de2f56.r2.cloudflarestorage.com

# Test Docker pull
docker pull mysql:8.0
```

## Alternative: Manual Image Pull with Registry Mirror

If DNS issues persist, you can configure Docker to use a registry mirror (if your network supports it).

## After Fixing DNS

Once DNS is working:
```powershell
docker-compose up --build
```

## Solution 6: Manual Image Import (If DNS Still Fails)

If DNS configuration doesn't work due to network restrictions, you can download images on another network and import them:

### On a network that works:
```powershell
docker save mysql:8.0 redis:7-alpine -o docker-images.tar
```

### On your current machine:
```powershell
docker load -i docker-images.tar
```

## Solution 7: Use Alternative Image Sources

If your university blocks Docker Hub, try using alternative registries or configure registry mirrors in `daemon.json`:

```json
{
  "registry-mirrors": ["https://mirror.gcr.io"]
}
```

## Verification Steps

1. **Check DNS resolution manually:**
   ```powershell
   nslookup docker-images-prod.6aa30f8b08e16409b46e0173d6de2f56.r2.cloudflarestorage.com 8.8.8.8
   ```

2. **Verify Docker is using correct DNS:**
   ```powershell
   docker info | findstr DNS
   ```

3. **Test image pull:**
   ```powershell
   docker pull mysql:8.0
   ```

## Critical: Restart Required

⚠️ **You MUST fully restart Docker Desktop for DNS changes to take effect!**

- Right-click Docker Desktop icon in system tray
- Click "Quit Docker Desktop"
- Wait for it to fully close (check Task Manager if unsure)
- Restart Docker Desktop
- Wait until it shows "Docker Desktop is running"

