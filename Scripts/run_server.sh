service cloudflared start

export DEPLOY_ENV=GLOBAL

cd ..
cp webXR/index.html templates/webXR.html
python app.py

service cloudflared stop