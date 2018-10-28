#!/bin/bash

# This script is an example to extract metadata using Singularity Python,
# Container Differ, and an image manifest. It's imperfect in trying
# to install software if not found, but should do well to exemplify the use
# case

exists () {
    type "$1" >/dev/null 2>/dev/null
}

# First argument should be Dockerfile

if [ "$#" -ne 1 ]
then
    echo "Usage: ./run_schemaorg_dockerfile.sh Dockerfile"
    exit 1
fi

################################################################################
# Step 1: metadata extraction
################################################################################

## Dockerfile (Singularity Python)

if [ ! -x "$(which spython)" ] ; then
    echo "Singularity python not found on path, installing with pip."
    pip install spython
fi

## Container Diff 

# If container-diff not on PATH, get it

if [ ! -x "$(which container-diff)" ] ; then
    echo "Container diff not found on PATH! Downloading to /tmp"
    curl -LO https://storage.googleapis.com/container-diff/latest/container-diff-linux-amd64
    chmod +x container-diff-linux-amd64
    mkdir -p /tmp/bin
    mv container-diff-linux-amd64 /tmp/bin/container-diff
    # export to bash environment
    export PATH="/tmp/bin:${PATH}"
fi

## Docker Image Manifest (ContainerImage)

docker pull "${CONTAINER_NAME}:${tag}";
                              docker inspect "${CONTAINER_NAME}:${tag}" > "${DOCKER_MANIFEST}";
                              /tmp/bin/container-diff-linux-amd64 analyze "${CONTAINER_NAME}:${tag}" --type=pip --type=file --type=apt --type=history --json > "inspect-${tag}.json";

## Docker Recipe Metadata (ContainerRecipe)
