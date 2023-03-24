#!/bin/bash

# go mod 改变更新基础镜像
function buildBase() {
    tmpF="./base_changed"
    localBaseHash=$(md5sum go.mod | awk '{print $1}')_$(md5sum go.sum | awk '{print $1}')
    if [ -f "$tmpF" ]; then
        oldHash=$(cat $tmpF)
        if [[ "${oldHash}" == "${localBaseHash}" ]]; then
            echo "The two strings are the same $oldHash"
            return 0
        fi
    fi
    tagName="blogapi_base:$(date '+%Y_%m_%d_%I_%M_%S')"
    tagNameLaster="blogapi_base:latest"
    if docker build -f ./deployment/base.Dockerfile -t "$tagNameLaster" -t "$tagName" .; then
        echo "$localBaseHash" >$tmpF
        printf "base image build success: %s" "$tagName"
    else
       echo "base image build fail!!!"
       exit 1
    fi
}

function build() {
    docker build -f ./deployment/dockerfile -t blogapi .
}

buildBase
build
