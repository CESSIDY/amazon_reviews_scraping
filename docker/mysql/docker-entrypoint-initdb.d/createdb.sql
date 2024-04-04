
### Sample as of real project with setting utf8mb4_unicode_ci on database level as default
CREATE USER IF NOT EXISTS 'scraper_user'@'%';
CREATE DATABASE IF NOT EXISTS `amazon_reviews_db` COLLATE 'utf8mb4_unicode_ci' ;
GRANT ALL ON `amazon_reviews_db`.* TO 'root'@'%' ;
GRANT ALL ON `amazon_reviews_db`.* TO 'scraper_user'@'%' ;

FLUSH PRIVILEGES ;
ALTER DATABASE `amazon_reviews_db` COLLATE 'utf8mb4_unicode_ci';
###

FLUSH PRIVILEGES ;