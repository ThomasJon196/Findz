source ../.env
# sudo cloudflared service install ${CLOUD_TOKEN}
sudo service cloudflared start

export DEPLOY_ENV=GLOBAL

cd ..
cp webXR/index.html templates/webXR.html
python app.py

sudo service cloudflared stop
echo "Stopped cloudflare daemon"