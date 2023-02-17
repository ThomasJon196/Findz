cd ../frontend
ng build --configuration production --build-optimizer

cd ..
rm -r static/*
mv frontend/dist/my-first-project/* static/
mv static/index.html templates/

cp webXR/index.html templates/webXR.html

python app.py