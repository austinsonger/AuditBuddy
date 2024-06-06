## ENVIRONMENT ##

#!/bin/bash

# Error tracking and logging function
log_error() {
    echo "Error: $1" >&2
}

# INSTALL JQ
mkdir -p $HOME/bin
curl -L https://github.com/stedolan/jq/releases/download/jq-1.6/jq-linux64 -o $HOME/bin/jq
if [ $? -ne 0 ]; then
    log_error "Failed to install jq"
    exit 1
fi
chmod +x $HOME/bin/jq
if [ $? -ne 0 ]; then
    log_error "Failed to set executable permission for jq"
    exit 1
fi