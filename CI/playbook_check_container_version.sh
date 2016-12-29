#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

function check_container_version {
    if [ "$TRAVIS_PULL_REQUEST_BRANCH" == "" ]; then
         echo "This check only for PR allowed, not for push."
         exit 0
    fi

    local branch=$TRAVIS_BRANCH
    SHELF='mirantis/bird-containers'

    DEF='roles/multirack/bird-container/defaults/main.yaml'
    CNT=$(cat $DEF | grep 'bgpd_container:' | awk '{print $2}')
    TAG=$(cat $DEF | grep 'bgpd_container_tag:' | awk '{print $2}')
    if [ $branch == "master" ]; then
        if [ $TAG != 'latest' ]; then
          echo "$DEF should contains 'bgpd_container_tag: latest', instead '$TAG' for branch '$branch'"
          exit 1
        fi
    elif [ "${branch:0:8}" == "release-" ]; then
        if [ $TAG != $branch ]; then
          echo "$DEF should contains 'bgpd_container_tag: $branch', instead '$TAG' for branch '$branch'"
          exit 1
        fi
    fi
    if [ $branch == "master" -o "${branch:0:8}" == "release-" ]; then
        if [ "$CNT" != "$SHELF" ]; then
          echo "bgpd_container should point to '$SHELF', instead '$CNT' for branch '$branch'"
          exit 1
        fi
    fi
}

check_container_version
