# Amazon reviews scraper

### **Description**

This scraper collects and stores reviews for the selected product, to change the product in the amazon_reviews.py spider, you need to change the product_code to the code of the desired product.


## **Requirements**
- Internet connection.
- Downloaded project source code (git clone https://github.com/CESSIDY/amazon_reviews_scraping/)
- Installed and running Docker
- Ensure, that needed for project ports are available (for running with Docker) (Mysql:3306) or change them on available.


### **Installation**
1. Rename the `.env.example` file name to `.env`:
   - Proxy settings (this scraper relies on rotating proxies for correct scraping, as Amazon will block it if the IP remains static.)
      - PROXY=some_host:some_port
      - PROXY_AUTH=some_username:some_password
      - PROXY_ENABLED=True
      - AUTO_CLOSE_CACHED_CONNECTIONS_ENABLED=False # If your proxy change it IP only after reconnection than this parameter need to be `True` for closing connection after every request. 
   - all other settings can remain the same, or you can change them as you wish (for example add your own Mysql database)

### **Running (After all configurations)**
  1. go to the project directory;
  2. run: `docker-compose build --force-rm`;
  3. run: `docker-compose up -d mysql` - if you use your own database you can skip this step 
  4. wait around 1 minute for completing DB initialization
  5. run: `docker-compose up -d python`


### **After launch**
You can test the scraper by connecting to `amazon_reviews_scraping-python-1` container (e.g. using Docker Desktop). also connect to Mysql database to view collected data.
