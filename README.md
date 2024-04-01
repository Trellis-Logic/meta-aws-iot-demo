# Overview

This project demonstrates the use of AWS IoT Jobs feature and Secure Tunneling on a Yocto
based build OS.

# AWS Environment setup

Refer to the [project wiki](https://github.com/Trellis-Logic/meta-aws-iot-demo/wiki) for details on setting up your AWS account
to support this project.

Add environment variables for your credentials and AWS IOT endpoints, either in the conf/kas/ yml file
or in the shell environment used for the build
```
export AWS_CREDENTIALS_ENDPOINT=<your credentials endpoint>
export AWSIOT_ENDPOINT=<your iot endpoint>
export BB_ENV_PASSTHROUGH_ADDITIONS="$BB_ENV_PASSTHROUGH_ADDITIONS AWSIOT_ENDPOINT AWS_CREDENTIALS_ENDPOINT"
```
Where `AWS_CREDENTIALS_ENDPOINT` is found from the command `aws iot describe-endpoint --endpoint-type iot:CredentialProvider` in
AWS Cloudshell or the aws command line and  `AWSIOT_ENDPOINT` is found in AWS Web console at AWSIoT->Settings.
Both of these strings should end with "amazonaws.com"

# Host Dependencies

* Install [yocto dependencies](https://docs.yoctoproject.org/brief-yoctoprojectqs/index.html#build-host-packages).
* Setup [kas](https://kas.readthedocs.io/en/latest/userguide.html) with
`pip3 install kas` or similar.
* Install bmaptool with `sudo apt-get update bmap-tools` or similar.

# Setup

```
git clone <path to repo>
```

# Building

```
./scripts/build-$machine.sh
```
where `$machine` is the machine you are building for (currently supported are `raspberrypi3` or `raspberrypi4-64`)

## Building with Docker

```
./scripts/build-docker $buildscript
```
where $buildscript is the `build-$machine.sh` script referenced above.

# Deploying

```
sudo ./scripts/deploy-$machine.sh /dev/sdX
```
where /dev/sdx is the device corresponding to your installed USB

# Deploying Certs

First create a .zip package containing the keys and certs from AWS when
creating the thing in AWSIot.

Name the zip file `thingname.zip` where `thingname` matches the name
of the thing in AWSIoT.

Then, use the path to this zip file as shown below.
```
./scripts/setup-device-certs <path to zip> <device IP>
```

# SSH and Device Update

Follow the instructions in [the wiki](https://github.com/Trellis-Logic/meta-aws-iot-demo/wiki) to configure and
demo AWS features.
