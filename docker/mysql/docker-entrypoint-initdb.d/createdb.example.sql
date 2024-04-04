#
# Copy createdb.sql.example to createdb.sql
# then uncomment then set database name and username to create you need databases
#
# example: .env MYSQL_USER=appuser and needed db name is myshop_db
#

#
#
# this sql script will auto run when the mysql container starts and the $DATA_PATH_HOST/mysql not found.
#
# if your $DATA_PATH_HOST/mysql exists and you do not want to delete it, you can run by manual execution:
#
#     docker-compose exec mysql bash
#     mysql -u root -p < /docker-entrypoint-initdb.d/createdb.sql
#

### Sample as of real project with setting utf8mb4_unicode_ci on database level as default
CREATE USER IF NOT EXISTS 'scraper_user'@'%';
CREATE DATABASE IF NOT EXISTS `amazon_reviews_db` COLLATE 'utf8mb4_unicode_ci' ;
GRANT ALL ON `amazon_reviews_db`.* TO 'root'@'%' ;
GRANT ALL ON `amazon_reviews_db`.* TO 'scraper_user'@'%' ;

FLUSH PRIVILEGES ;
ALTER DATABASE `amazon_reviews_db` COLLATE 'utf8mb4_unicode_ci';
###

FLUSH PRIVILEGES ;