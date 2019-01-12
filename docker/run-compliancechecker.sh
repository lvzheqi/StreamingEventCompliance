#!/bin/bash

docker run --name compliancechecker --link mysqldb -p 5000:5000 streameventcompliance
