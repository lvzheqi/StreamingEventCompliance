## BUILD & RUN ON DOCKER


#### Method 1
1. Run `sh build-run-db.sh` to pull the mysql:5.7 database and create `mysqldb` container.

2. Run `sh build-compliancechecker.sh` to build `streameventcompliance` image.

3. Run `sh run-compliancechecker.sh` to create `compliancechecker` container.

(4.) Run `sh clean-compliancechecker.sh` to stop and remove `compliancechecker` container.


#### Method 2
using docker-compose

Execute `docker-compose up` to build and run the project directly.
（Once the project is killed, the MySQL container will also be killed）

For MAC:
If you want to link to the database in you own computer, then set `hostname = docker.for.mac.host.internal` 
and map container port 33060 to local MySQL port (Default 3306).


Tip: all the commands run under this directory path.