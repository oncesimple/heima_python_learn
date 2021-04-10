#!/bin/bash

sudo systemctl restart docker
docker pull mysql:5.7
docker run -p 12345:3306 --name mysql -v /mysql/conf:/etc/mysql/conf.d -v /mysql/logs:/logs -v /mysql/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 -d --privileged=true mysql:5.7