#!/bin/bash
command = $1
if [ -z "$command" ]; then
    command=build-raspberrypi3.sh
    echo "Please specify build command as first argument, defaulting to ${command}"
fi
scriptsdir=$(realpath $(dirname $0))
pushd $(dirname $0)/../../
mkdir -p builddir
docker run -v $(pwd):$(pwd) \
        --workdir $(pwd) \
        --user $(id -u):$(id -g) \
        --entrypoint ${scriptsdir}/$command \
        ghcr.io/siemens/kas/kas:latest 
