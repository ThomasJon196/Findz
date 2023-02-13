cd ..

# Load env variables (Source file by executing its commands in current shell )
source .env

curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb 

sudo dpkg -i cloudflared.deb

sudo cloudflared service install $CLOUD_TOKEN