#!/bin/sh
set -ex
test -d downloads || mkdir downloads
cd downloads
wget https://ftp.mozilla.org/pub/firefox/releases/45.2.0esr/firefox-45.2.0esr.linux-x86_64.sdk.tar.bz2
tar -xjf firefox-45.2.0esr.linux-x86_64.sdk.tar.bz2
