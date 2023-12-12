#!/bin/bash

wget https://ftp.gnu.org/gnu/mit-scheme/stable.pkg/12.1/mit-scheme-12.1-aarch64le.tar.gz

tar xzf mit-scheme-12.1-aarch64le.tar.gz

cd ./mit-scheme-12.1/src

bash ./configure

make

make install

cd ../doc
./configure
make