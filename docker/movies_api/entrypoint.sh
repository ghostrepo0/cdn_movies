#!/usr/bin/env sh

set -o errexit
set -o nounset

readonly cmd="$*"

redis_elastic_ready () {
  # Check that postgres is up and running on port `5432`:
  dockerize -wait "tcp://${REDIS_HOST}:${REDIS_PORT}" -wait "http://${ELASTICSEARCH_HOST}:${ELASTICSEARCH_PORT}"  -timeout 10s
}

# We need this line to make sure that this container is started
# after the one with postgres, redis and elastic
until redis_elastic_ready; do
  >&2 echo '--- WAITING --- Redis, Elastic are connecting...'
done

>&2 echo '--- CONNECTED --- Redis, Elastic are ready!'

# Evaluating passed command (do not touch):
# shellcheck disable=SC2086
exec $cmd
