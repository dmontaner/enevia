#!/bin/bash
# setup_ubuntu_desktop_app.sh
# 2021-06-28 david.montaner@gmali.com
# install the desktop app in ubuntu

sudo cp ../splitpdf.py /usr/bin/splitpdf
sudo chmod +x /usr/bin/splitpdf

sudo cp enevia_logo.png /usr/share/icons/
sudo cp enevia.desktop  /usr/share/applications
