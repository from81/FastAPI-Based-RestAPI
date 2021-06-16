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
<clone this repo>
pip install -r requirements.txt

# Data

- OSM Australia
- boundary: https://www.igismap.com/australia-shapefile-download/
- neighborhood: https://data.gov.au/data/dataset/nsw-local-government-areas
