#!/bin/bash
base_repo_path=$(realpath $(dirname $0))/../
cd ${base_repo_path}/..
base=$(basename $0 .sh)
machine="${base##*-}"
if [ ! -z "${machine}" ]; then
    echo "building for machine ${machine}"
    export KAS_MACHINE=${machine}
fi
kas build --update ${base_repo_path}/conf/kas/rpi3-rauc-aws.yml
