import os
from distutils.util import strtobool

from dotenv import load_dotenv

load_dotenv()

BOT_NAME = "scraper"

SPIDER_MODULES = ["scraper.spiders"]
NEWSPIDER_MODULE = "scraper.spiders"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 16

#DOWNLOAD_DELAY = 3

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "User-Agent": USER_AGENT,
}

RETRY_TIMES = 3
RETRY_HTTP_CODES = [302, 500, 502, 503, 504]

DOWNLOAD_HANDLERS = {
    'http': 'scraper.utils.handlers.RotatingProxiesDownloadHandler',
    'https': 'scraper.utils.handlers.RotatingProxiesDownloadHandler'
}

DOWNLOADER_MIDDLEWARES = {
    "scraper.middlewares.HttpProxyMiddleware": 500,
    # "scrapy.downloadermiddlewares.retry.RetryMiddleware": 501
    "scraper.middlewares.CustomRetryMiddleware": 501,
}

EXTENSIONS = {
    "scrapy.extensions.telnet.TelnetConsole": None,
}

ITEM_PIPELINES = {
    "scraper.pipelines.ReviewsStoringPipeline": 300,
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE") if os.getenv("LOG_FILE", "") else None

ROTATING_PROXIES_DOWNLOADER_HANDLER_AUTO_CLOSE_CACHED_CONNECTIONS_ENABLED = strtobool(
    os.getenv("AUTO_CLOSE_CACHED_CONNECTIONS_ENABLED", "False")
)

PROXY = os.getenv("PROXY", "")
PROXY_AUTH = os.getenv("PROXY_AUTH", "")
PROXY_ENABLED = strtobool(os.getenv("PROXY_ENABLED", "False"))

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USERNAME = os.getenv("DB_USERNAME", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_DATABASE = os.getenv("DB_DATABASE", "db_name")
