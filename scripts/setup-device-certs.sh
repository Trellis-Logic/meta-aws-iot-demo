#!/bin/bash
certs_pkg=$1
device=$2

usage()
{
    echo "$0 [certs_pkg] [dev]"
    echo "Write the certs from the AWS package at [certs_pkg] to the device at [dev]"
    echo "Assume the certs package name is in the form of <thingname>.zip or directory named <thingname>"
    echo "or alternatively, includes an "device-environment.txt" containing the thing name as an"
    echo "environment value AWSIOT_THING_NAME"
}
if [ -z "${certs_pkg}" ]; then
    echo "Please specify a cert package as first argument"
    usage
    exit 1
fi
if [ -z "${device}" ]; then
    echo "Please specify a device as second argument"
    usage
    exit 1
fi
set -e
tmpbase=$(mktemp -d aws-iot-deploy-certs.XXXX)
if [[ ${certs_pkg} == *.zip ]]; then
    unzip ${certs_pkg} -d ${tmpbase}
elif [[ ${certs_pkg} == *.tar.gz ]]; then
    tar -xvf ${certs_pkg} -C ${tmpbase}
else
    cp -r ${certs_pkg}/* ${tmpbase}
fi
filename=$(basename ${certs_pkg%.*})
tmpdir=${tmpbase}/${filename}
if [ ! -e ${tmpdir}/AmazonRootCA1.pem ]; then
    mv ${tmpdir}/Amazon*.pem ${tmpdir}/AmazonRootCA1.pem
fi
chmod 644 ${tmpdir}/AmazonRootCA1.pem
if [ ! -e ${tmpdir}/device.pem.crt ]; then
    mv ${tmpdir}/*.pem.crt ${tmpdir}/device.pem.crt
fi
chmod 644 ${tmpdir}/device.pem.crt
if [ ! -e ${tmpdir}/private.pem.key ]; then
    mv ${tmpdir}/*-private.pem.key ${tmpdir}/private.pem.key
fi
chmod 600 ${tmpdir}/private.pem.key
if [ ! -e ${tmpdir}/device-environment.env ]; then
    echo "AWSIOT_THING_NAME=${filename}" > ${tmpdir}/device-environment.env
fi
chmod 644 ${tmpdir}/device-environment.env
echo "Copying ${tmpdir} content to ${device}"
scp -p ${tmpdir}/* root@${device}:/etc/aws-iot-device-client/thing/
rm -rf ${tmpdir}
