# Amazon reviews scraper

### **Description**

This scraper collects and stores reviews for the selected product, to change the product in the `amazon_reviews.py` spider, you need to change the `product_code` to the code of the desired product.


## **Requirements**
- Internet connection.
- Downloaded project source code (git clone https://github.com/CESSIDY/amazon_reviews_scraping/)
- Installed and running Docker
- Ensure, that needed for project ports are available (for running with Docker) (Mysql:3306) or change them on available.


### **Installation**
1. Rename the `.env.example` file name to `.env`:
   - Proxy settings (this scraper relies on rotating proxies for correct scraping, as Amazon will block it if the IP remains static.)
      - `PROXY`=some_host:some_port
      - `PROXY_AUTH`=some_username:some_password
      - `PROXY_ENABLED`=True
   - For Scrapy: 
     - `AUTO_CLOSE_CACHED_CONNECTIONS_ENABLED`=False # If your proxy change it IP only after reconnection than this parameter need to be `True` for closing connection after every request. 
   - For Botasaurus:
     - `SSL_CERT_CHECK_ENABLED`=True # If you have a problem with the ssl certificate validation when using a proxy, then you can disable (`False`) the SSL certificate validation to work around the problem (but it leaves you vulnerable to some security threats)
   - all other settings can remain the same, or you can change them as you wish (for example add your own Mysql database)

### **Running (After all configurations)**
  1. go to the project directory;
  2. run: `docker-compose build --force-rm`;
  3. run: `docker-compose up -d mysql` - if you use your own database you can skip this step 
  4. wait around 1 minute for completing DB initialization
  5. several implementations of scrapers to choose from:
     - run: `docker-compose up -d scraper-scrapy` basic scrapy scraper (need to use rotation proxy)
     - run: `docker-compose up -d scraper-botasaurus-request` a more inconspicuous scraper (but also better use a rotation proxy)


### **After launch**
You can see the scraping progress by connecting to the Docker container of the scraper you launched [`amazon_reviews_scraping-scraper-botasaurus-request`, `amazon_reviews_scraping-scraper-scrapy`] (e.g. using Docker Desktop), also connect to Mysql database to view collected data.
