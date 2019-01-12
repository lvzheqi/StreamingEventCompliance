## BUILD & RUN ON DOCKER


#### Method 1
1. Run `sh build-run-db.sh` to pull the mysql:5.7 database and create `mysqldb` container.

2. Run `sh build-compliancechecker` to build `streameventcompliance` image.

3. Run `sh run-compliancechecker` to create `compliancechecker` container.

(4.) Run `sh clean-compliancechecker` to stop and remove `compliancechecker` container.


#### Method 2
using docker-compose

Execute `docker-compose up` to build and run the project directly.
（Once the project is killed, the MySQL container will also be killed）

Tip: all the commands run under this directory path.