cd /var/app

poetry run alembic upgrade head
poetry run scrapy crawl amazon_reviews_botasaurus_request
