# Fix Docker DNS via Docker Desktop GUI

## The Problem
Docker cannot resolve Cloudflare storage domains on your university network. The `daemon.json` DNS settings may not work for image pulling.

## Solution: Use Docker Desktop GUI Settings

### Step-by-Step Instructions:

1. **Open Docker Desktop**
   - Look for the Docker icon in your system tray (bottom right)
   - Double-click to open, or right-click and select "Open Docker Desktop"

2. **Open Settings**
   - Click the **gear icon** (⚙️) in the top-right corner of Docker Desktop window

3. **Navigate to Network Settings**
   - In the left sidebar, click **Resources**
   - Then click **Network** (or look for DNS settings)

4. **Configure DNS**
   - Find the **DNS Server** setting
   - Change from **"Automatic"** to **"Manual"**
   - Enter the following DNS servers (one per line or comma-separated):
     ```
     8.8.8.8
     8.8.4.4
     ```
   - OR use Cloudflare DNS:
     ```
     1.1.1.1
     1.0.0.1
     ```

5. **Apply Changes**
   - Click **"Apply & Restart"** button
   - Wait for Docker Desktop to restart completely
   - You'll see "Docker Desktop is running" when it's ready

6. **Test**
   ```powershell
   docker pull mysql:8.0
   ```

## Alternative: If GUI Settings Don't Exist

Some Docker Desktop versions may not have this setting. In that case:

### Option A: Change System DNS

1. Open **Network Settings**
   - Press `Win + I` → **Network & Internet** → **Advanced network settings** → **More network adapter options**
   - OR right-click network icon → **Open Network & Internet settings** → **Change adapter options**

2. Right-click your active network connection → **Properties**

3. Select **Internet Protocol Version 4 (TCP/IPv4)** → **Properties**

4. Select **"Use the following DNS server addresses"**:
   - Preferred DNS server: `8.8.8.8`
   - Alternate DNS server: `8.8.4.4`

5. Click **OK** and restart Docker Desktop

### Option B: Use Windows Hosts File (Temporary Workaround)

If DNS is completely blocked, you can try adding entries to `C:\Windows\System32\drivers\etc\hosts`:

```powershell
# Run PowerShell as Administrator
notepad C:\Windows\System32\drivers\etc\hosts
```

However, this won't work for dynamic Cloudflare domains.

### Option C: Use VPN or Mobile Hotspot

- Connect to a VPN that bypasses university network restrictions
- OR use your mobile phone's hotspot temporarily

### Option D: Pre-download Images Elsewhere

1. On a network that works (home, mobile hotspot, etc.):
   ```powershell
   docker pull mysql:8.0
   docker pull redis:7-alpine
   docker save mysql:8.0 redis:7-alpine -o docker-images.tar
   ```

2. Transfer `docker-images.tar` to your university machine

3. Load the images:
   ```powershell
   docker load -i docker-images.tar
   ```

4. Then run `docker-compose up --build` (it will use the loaded images)

## Verification

After applying DNS changes, verify:

```powershell
# Test DNS resolution
nslookup docker-images-prod.6aa30f8b08e16409b46e0173d6de2f56.r2.cloudflarestorage.com 8.8.8.8

# Test Docker pull
docker pull mysql:8.0
```

If both work, then run:
```powershell
docker-compose up --build
```

