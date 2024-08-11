#!/bin/bash

# Give validator alpha some time to start up
if [ "$HOSTNAME" != "validator_alpha" ] && [ "$HOSTNAME" != "pos-blockchain-validator_alpha-1" ]; then
  echo "Waiting for validator_alpha to start up..."
  sleep 10
fi

exec "$@"