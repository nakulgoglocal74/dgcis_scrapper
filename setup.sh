#!/bin/bash
echo [$(date)]: 'START'

echo [$(date)]: 'CD into project folder'
cd /home/nakul/projects/DGCIS

echo [$(date)]: 'Activate ENV'
source "/home/nakul/projects/envs/srapper_selenium/bin/activate"

echo [$(date)]: 'Removing previous logs'
rm -rf /home/nakul/projects/DGCIS/__public_logs__/*

echo [$(date)]: 'Killing port 8000'
sudo kill -9 `sudo lsof -t -i:8000`

echo [$(date)]: 'Checking nginx installation'
if [ "$(dpkg -l | awk '/nginx/ {print }'|wc -l)" -ge 1 ];
then  
    echo [$(date)]: 'Package nginx already present. Skipping installation...'
else
    echo [$(date)]: 'Package nginx not present. Installing it...'
    sudo apt install nginx
fi

echo [$(date)]: 'Updating nginx file'
sudo echo "server {
    listen 80;
    server_name $(curl icanhazip.com);
    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}" > /etc/nginx/sites-enabled/fastapi_nginx

echo [$(date)]: 'Restarting nginx service'
sudo service nginx restart

echo [$(date)]: 'Starting uvicorn service'
nohup uvicorn main:app --host 0.0.0.0 --port 8000 --reload >> __public_logs__/out 2>> __public_logs__/error &

echo [$(date)]: 'END'