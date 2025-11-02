# Fix Docker DNS via Docker Engine Settings

Since your Docker Desktop doesn't have DNS settings in the Network section, we'll use the **Docker Engine** settings to add DNS configuration directly.

## Step-by-Step Instructions:

1. **In Docker Desktop Settings:**
   - You're currently in **Resources** → **Network**
   - Click **"Docker Engine"** in the left sidebar (below "Resources")

2. **Edit the JSON Configuration:**
   - You'll see a JSON editor with Docker daemon configuration
   - Find the existing configuration (it might look like `{}` or have some settings)
   
3. **Add DNS Configuration:**
   - Add the `"dns"` property to the JSON
   - Your configuration should look like this:
   
   ```json
   {
     "builder": {
       "gc": {
         "defaultKeepStorage": "20GB",
         "enabled": true
       }
     },
     "experimental": false,
     "dns": ["8.8.8.8", "8.8.4.4"]
   }
   ```

4. **Apply Changes:**
   - Click **"Apply & Restart"** button
   - Wait for Docker Desktop to restart completely
   - You'll see "Docker Desktop is running" when ready

5. **Test:**
   ```powershell
   docker pull mysql:8.0
   ```

## Alternative: If Docker Engine Settings Don't Work

If editing Docker Engine settings doesn't work or the changes don't persist, try changing **System DNS** instead:

1. **Open Network Settings:**
   - Press `Win + I` → **Network & Internet** → **Advanced network settings** → **More network adapter options**
   - OR right-click network icon → **Open Network & Internet settings** → **Change adapter options**

2. **Configure DNS:**
   - Right-click your **Wi-Fi** adapter → **Properties**
   - Select **Internet Protocol Version 4 (TCP/IPv4)** → **Properties**
   - Select **"Use the following DNS server addresses"**
   - Preferred: `8.8.8.8`
   - Alternate: `8.8.4.4`
   - Click **OK**

3. **Restart Docker Desktop:**
   - Right-click Docker Desktop system tray icon → **Quit Docker Desktop**
   - Restart Docker Desktop

4. **Test:**
   ```powershell
   docker pull mysql:8.0
   ```

## Last Resort: Pre-download Images

If DNS changes don't work, download images on another network:

1. **On a network that works:**
   ```powershell
   docker pull mysql:8.0
   docker pull redis:7-alpine
   docker save mysql:8.0 redis:7-alpine -o docker-images.tar
   ```

2. **Transfer `docker-images.tar` to your machine**

3. **Load images:**
   ```powershell
   docker load -i docker-images.tar
   docker-compose up --build
   ```

