export DEPLOY_ENV=LOCAL

cd ..
pip3 install -r requirements.txt
cp webXR/index.html templates/webXR.html
python3 app.py

