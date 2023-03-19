export DEPLOY_ENV=LOCAL

cd ../frontend
ng build --configuration production --build-optimizer

cd ..
rm -r static/*
mv frontend/dist/my-first-project/* static/
mv static/index.html templates/
cp -r images/* static/

cp webXR/index.html templates/webXR.html

python app.py