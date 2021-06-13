#!/bin/bash

# Setup a cronjob to run this script at your desired interval
# install httping (https://zoomadmin.com/HowToInstall/UbuntuPackage/httping)
httping  -c 1  localhost:5000/check
