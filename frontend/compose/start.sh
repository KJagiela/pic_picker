#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

envsubst < /default.conf > /etc/nginx/conf.d/default.conf
nginx -g "daemon off;"
