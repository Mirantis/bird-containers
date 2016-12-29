#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

if [ "$TRAVIS_PULL_REQUEST_BRANCH" != "" ]; then
     echo "Build of container skipped for PR. Container will be builded and uploaded after merge."
     exit 0
fi

DATE=$(date "+%Y%m%d")
WD="$(pwd)/bird-container/tmp-$DATE"

cd bird-container
make build-container

IMG_ID=$(tail -n 10 $WD/build.log  | grep 'Successfully built' | awk '{print $3}')

if [ "$IMG_ID" == "" ] ; then
    echo "Container was not successfully built."
    exit 1
fi
