DESCRIPTION = "AWS RAUC demo image"

IMAGE_FEATURES += "ssh-server-openssh"

inherit core-image

CORE_IMAGE_BASE_INSTALL += "aws-jobs"
