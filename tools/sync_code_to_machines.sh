#!/bin/bash

set -e

CLOUD_NAME=${CLOUD_NAME:-"hetzner"}

SCRIPT=$(realpath "$0")
SCRIPT_PATH=$(dirname "$SCRIPT")

CONTAINER_TO_BENCH=${CONTAINER_TO_BENCH:-"qdrant-single-node"}


BENCH_SERVER_NAME=${SERVER_NAME:-"benchmark-server-1"}
BENCH_CLIENT_NAME=${CLIENT_NAME:-"benchmark-client-1"}


IP_OF_THE_SERVER=$(bash "${SCRIPT_PATH}/${CLOUD_NAME}/get_public_ip.sh" "$BENCH_SERVER_NAME")
IP_OF_THE_CLIENT=$(bash "${SCRIPT_PATH}/${CLOUD_NAME}/get_public_ip.sh" "$BENCH_CLIENT_NAME")

bash -x "${SCRIPT_PATH}/sync.sh" "root@$IP_OF_THE_SERVER"
bash -x "${SCRIPT_PATH}/sync.sh" "root@$IP_OF_THE_CLIENT"

cat "${SCRIPT_PATH}/install_dependencies.sh" | ssh "root@${IP_OF_THE_CLIENT}" bash

bash -x "${SCRIPT_PATH}/run_server_container.sh" "$CONTAINER_TO_BENCH"

