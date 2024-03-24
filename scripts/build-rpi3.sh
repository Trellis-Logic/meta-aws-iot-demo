#!/bin/sh
base_repo_path=$(realpath $(dirname $0))/../
cd ${base_repo_path}/..
kas build --update ${base_repo_path}/conf/kas/rpi3-rauc-aws.yml
