P_KEY=$(jq -r '.pem' $1)
API_HOST=$(jq -r '.api_host' $1)

ssh -i $P_KEY ubuntu@$API_HOST