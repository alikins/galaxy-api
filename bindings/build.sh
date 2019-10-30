#!/bin/bash

bindings_dir=$(dirname $(readlink -f "$0"))

docker run --rm -u "$(id -u)" -v "${bindings_dir}:/local" \
  openapitools/openapi-generator-cli generate \
  -t /local/openapi-templates/python \
  -i /local/openapi.yaml \
  -g python \
  -o /local/galaxy-pulp \
  --skip-validate-spec \
  --additional-properties=packageName=galaxy_pulp,projectName=galaxy-pulp
