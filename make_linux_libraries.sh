#!/bin/sh

DEST_DIR=libusb_package_tng/libraries
LIBUSB_VERS=1.0.29

echo 'Building Docker images...'
docker build --platform linux/aarch64 -t libusb_manylinux2014_aarch64 -f dockerfiles/Dockerfile_manylinux2014_aarch64 .
docker build --platform linux/386     -t libusb_manylinux2014_i686    -f dockerfiles/Dockerfile_manylinux2014_i686    .
docker build --platform linux/amd64   -t libusb_manylinux2014_x86_64  -f dockerfiles/Dockerfile_manylinux2014_x86_64  .
docker build --platform linux/arm/v7  -t libusb_musllinux_1_2_armv7l  -f dockerfiles/Dockerfile_musllinux_1_2_armv7l  .
docker build --platform linux/arm/v7  -t libusb_debian_10_armv7l      -f dockerfiles/Dockerfile_debian_10_armv7l      .

echo 'Copying libraries into place...'
docker run --platform linux/aarch64 -ti --rm --mount type=bind,source="$(pwd)",target=/mnt/bind-root libusb_manylinux2014_aarch64 \
    /bin/bash -c "cp /root/libusb/libusb/.libs/libusb-1.0.so $DEST_DIR/libusb-linux-arm64-$LIBUSB_VERS.so && strip $DEST_DIR/libusb-linux-arm64-$LIBUSB_VERS.so"
docker run --platform linux/386 -ti --rm --mount type=bind,source="$(pwd)",target=/mnt/bind-root libusb_manylinux2014_i686 \
    /bin/bash -c "cp /root/libusb/libusb/.libs/libusb-1.0.so $DEST_DIR/libusb-linux-i686-$LIBUSB_VERS.so && strip $DEST_DIR/libusb-linux-i686-$LIBUSB_VERS.so"
docker run --platform linux/amd64 -ti --rm --mount type=bind,source="$(pwd)",target=/mnt/bind-root libusb_manylinux2014_x86_64 \
    /bin/bash -c "cp /root/libusb/libusb/.libs/libusb-1.0.so $DEST_DIR/libusb-linux-x86_64-$LIBUSB_VERS.so && strip $DEST_DIR/libusb-linux-x86_64-$LIBUSB_VERS.so"
docker run --platform linux/arm/v7 -ti --rm --mount type=bind,source="$(pwd)",target=/mnt/bind-root libusb_musllinux_1_2_armv7l \
    /bin/bash -c "cp /root/libusb/libusb/.libs/libusb-1.0.so $DEST_DIR/libusb-musl-armv7l-$LIBUSB_VERS.so && strip $DEST_DIR/libusb-musl-armv7l-$LIBUSB_VERS.so"
docker run --platform linux/arm/v7 -ti --rm --mount type=bind,source="$(pwd)",target=/mnt/bind-root libusb_debian_10_armv7l \
    /bin/bash -c "cp /root/libusb/libusb/.libs/libusb-1.0.so $DEST_DIR/libusb-debian-10-armv7l-$LIBUSB_VERS.so && strip $DEST_DIR/libusb-debian-10-armv7l-$LIBUSB_VERS.so"
