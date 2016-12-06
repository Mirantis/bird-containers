#!/bin/sh
set -x
cd /bird_src
./configure --prefix=/usr --sysconfdir=/etc --mandir=/usr/share/man --localstatedir=/var
make
