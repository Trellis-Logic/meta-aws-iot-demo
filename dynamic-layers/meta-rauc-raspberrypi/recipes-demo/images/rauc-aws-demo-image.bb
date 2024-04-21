DESCRIPTION = "AWS RAUC demo image"

IMAGE_FEATURES += "ssh-server-openssh"

inherit core-image

CORE_IMAGE_BASE_INSTALL += "aws-jobs"

inherit extrausers
# See https://docs.yoctoproject.org/singleindex.html#extrausers-bbclass
# We set a default password of root to support password login from AWS
# SSH console, which requires a password.
# Don't do this in a production image
# PASSWD below is set to the output of
# printf "%q" $(mkpasswd -m sha256crypt root) to hash the "root" password
# string
PASSWD = "\$5\$2WoxjAdaC2\$l4aj6Is.EWkD72Vt.byhM5qRtF9HcCM/5YpbxpmvNB5"
EXTRA_USERS_PARAMS = "usermod -p '${PASSWD}' root;"
