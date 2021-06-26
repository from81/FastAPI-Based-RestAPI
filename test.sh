# script for integration test
# deployes postgis docker 
set -e
source ~/opt/anaconda3/etc/profile.d/conda.sh
docker build -t postgis_image -f ./Dockerfile_postgis .
docker container run -d --publish 5432:5432 --env-file ./.env --name postgis postgis_image /bin/bash -c 'while [ 1 ]; do sleep 30; done;'
sleep 240
conda activate geoapi
# pytest --verbose --color=yes --cov=app
# docker container stop postgis
# docker container rm postgis

(pytest --verbose --color=yes --cov=app && docker container stop postgis && docker container rm postgis) || (docker container stop postgis && docker container rm postgis)