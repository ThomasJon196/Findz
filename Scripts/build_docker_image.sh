
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
  set DOCKER_BUILDKIT=1

else
  export DOCKER_BUILDKIT=1
fi

cd ..
docker build -t findz-flask-server .