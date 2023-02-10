# Build current angular html/css/js files
# Copy files into static & templates folder for flask server

cd ../frontend
# ng build --configuration production --build-optimizer

cd ..
touch test
mv frontend/dist/my-first-project/* static/
mv static/index.html templates/