source ../.env
# sudo cloudflared service install ${CLOUD_TOKEN}
service cloudflared start

export DEPLOY_ENV=GLOBAL

cd ..
cp webXR/index.html templates/webXR.html
python app.py

service cloudflared stop