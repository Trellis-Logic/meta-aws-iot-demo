SRC_URI += " \
            file://update-image.py \
"

LICENSE="MIT"
LIC_FILES_CHKSUM ?= "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

do_install() {
    install -d 700 -d ${D}/sbin/aws-iot-device-client-handlers/
    install -m 700 ${WORKDIR}/update-image.py ${D}/sbin/aws-iot-device-client-handlers/
}

RDEPENDS:${PN} += "aws-iot-device-client"
RDEPENDS:${PN} += "python3"
RDEPENDS:${PN} += "python3-core"
RDEPENDS:${PN} += "python3-boto3"
RDEPENDS:${PN} += "python3-requests"
