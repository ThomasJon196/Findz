source ../.env
# sudo cloudflared service install ${CLOUD_TOKEN}

sudo cloudflared service install $CLOUD_TOKEN_2
sudo service cloudflared start
echo "Started cloudflare daemon"

export DEPLOY_ENV=GLOBAL_2

cd ..
cp webXR/index.html templates/webXR.html
python app.py

sudo service cloudflared stop
sudo cloudflared service uninstall
echo "Uninstalled cloudflare daemon"