#!/bin/bash
git clone https://github.com/Asylumrunner/Hedrographer.git
apt-get update
apt-get install -y python3-pip
apt-get install -y awscli
apt-get install -y npm
npm install pm2@latest -g
cd Hedrographer
pip3 install --user -r requirements.txt
aws s3 cp s3://hedrographer/secrets.py secrets.py
pm2 start bot.py --name Hedrographer --interpreter python3
