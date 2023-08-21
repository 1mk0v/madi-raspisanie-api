#!/bin/bash

python3 -m venv env
echo 'Virtual Envirement is created'
source env/bin/activate
echo 'Virtual Envirement is activated'
pip3 install -r requirements.txt
echo 'Requirements is installed'
