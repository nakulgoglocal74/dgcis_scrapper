#!/bin/bash
nginx_port=8000
app_port=$((nginx_port + 1))
project_path=/home/nakul/projects/DGCIS
env_path=/home/nakul/projects/envs/srapper_selenium/bin/activate
url_file_path=/home/nakul/projects/app_urls.txt

echo [$(date)]: "START"

echo [$(date)]: "CD into project folder"
cd $project_path

echo [$(date)]: "Activate ENV"
source $env_path

echo [$(date)]: "Removing previous logs"
rm -rf __public_logs__/
mkdir __public_logs__/

echo [$(date)]: "Killing app port ${app_port}"
sudo kill -9 $(lsof -i:${app_port} -t)

echo [$(date)]: "Killing nginx port ${nginx_port}"
sudo kill -9 $(lsof -i:${nginx_port} -t)

echo [$(date)]: "Updating nginx file"
sudo echo "server {
    listen ${nginx_port};
    server_name $(curl icanhazip.com);
    location / {
        proxy_pass http://127.0.0.1:${app_port};
    }
}" > /etc/nginx/sites-enabled/fastapi_nginx

echo [$(date)]: "Starting uvicorn service"
nohup uvicorn main:app --host 0.0.0.0 --port $app_port --reload >> __public_logs__/out 2>> __public_logs__/error &

echo [$(date)]: "App started"
echo "DGCIS:http://$(curl icanhazip.com):$nginx_port" > $url_file_path

echo [$(date)]: "END"