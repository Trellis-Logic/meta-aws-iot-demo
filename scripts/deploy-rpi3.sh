#!/bin/sh

sdcard=$1
if [ -z "$sdcard" ]; then
    echo "Please specify path to sdcard as first argument"
    exit 1
fi
if [ ! -b "$sdcard" ]; then
    echo "$sdcard is not a block device."
    echo "Please specify path to sdcard as first argument"
    exit 1
fi
cd $(dirname $0)/../
imgfile=../build/tmp/deploy/images/raspberrypi3/rauc-aws-demo-image-raspberrypi3.wic.bz2
if [ ! -e "$imgfile" ]; then
    echo "$imgfile does not exist, please build first"
    exit 1
fi

echo "Writing $imgfile to $sdcard - this will take a few minutes"
bmaptool copy $imgfile $sdcard

echo "Ejecting $sdcard"
eject $sdcard
