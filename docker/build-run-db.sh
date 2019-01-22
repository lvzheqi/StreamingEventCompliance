#!/bin/bash

# docker pull mysql:5.7
docker run --name mysqldb -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=compliancechecker -e MYSQL_USER=compliancechecker -e MYSQL_PASSWORD=compliancechecker -d mysql:5.7
