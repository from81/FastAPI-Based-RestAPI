make `psql.sh` executable
`chmod +x psql.sh`

connect to db (requires installation of [jq](https://stedolan.github.io/jq/)):
`./psql.sh credentials_prod.json`

# Setting up API server on EC2
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python-pip
sudo apt-get install python3.9
alias python=python3

sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 2
sudo update-alternatives --config python3
git clone https://github.com/from81/FastAPI-Based-RestAPI.git
pip install -r requirements.txt

# Data

- OSM Australia
- boundary: https://www.igismap.com/australia-shapefile-download/
- neighborhood: https://data.gov.au/data/dataset/nsw-local-government-areas

# Rest API

## Todo
- ecs / fargate
- hashicorp vault
- neighborhood
    - get n districts and distance, sorted by proximity
- poi
    - get nearest n poi, optionally filtered by category/s, sorted by distance and with google link
- use router
- try/catch
- use pydantic.basemodel
- https://online.sqlfluff.com/

## Run
`python main.py`
or
`uvicorn main:app --reload`

```
docker build -t geoapiv1 ./

docker container run --publish 80:80 --detach --env-file ./.env --name <container_name> <image_name>
docker container run --publish 80:80 --detach --env-file ./.env --name geoapi geoapiv1
docker container run --publish 80:80 --env-file ./.env --name geoapi geoapiv1

```