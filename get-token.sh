#!/bin/zsh

TOKEN=$(curl -s \
  -d "client_id=fuel-api" \
  -d "client_secret=XUa7r2PrOQjNancsL1KXyW4lrXKtjoMx" \
  -d "grant_type=client_credentials" \
  http://localhost:8080/realms/fuel-insights/protocol/openid-connect/token | jq -r .access_token)

echo $TOKEN

