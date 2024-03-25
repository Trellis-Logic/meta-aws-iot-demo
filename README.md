# Overview

This project demonstrates the use of AWS IoT Jobs feature and Secure Tunneling on a Yocto
based build OS.

# AWS Environment setup

Refer to the wiki page at TODO for details on setting up your AWS account to support the 

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
./scripts/build-rpi3.sh
```

# Deploying

```
sudo ./scripts/deploy-rpi3.sh /dev/sdX
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

# Remote device update using AWS Jobs

1. Follow the instructions in [TBD] to setup policies and IAM roles
which allow fetch from S3 bucket using credentials obtained from
device key and cert.
2. Upload this job document to an S3 bucket and use it to create
and run an AWS Job:
```
{
    "_comment": "This sample JSON file can be used for performing an image update on a device.",
    "version": "1.0",
    "steps": [
        {
            "action": {
                "name": "Update-Image",
                "type": "runCommand",
                "input": {
                    "command": "/sbin/aws-iot-device-client-handlers/update-image.py,s3://your-bucket/your-update-file"
                },
                "runAsUser": "root"
            }
        }
    ]
}
```
Where `s3://your-bucket/your-update-file` is the S3 URI of an update image file found in the
build artifacts.
