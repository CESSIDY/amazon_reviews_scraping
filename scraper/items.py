import scrapy


class ReviewItem(scrapy.Item):
    product_code = scrapy.Field()
    external_id = scrapy.Field()

    review_body = scrapy.Field()
    rating_number = scrapy.Field()
    author = scrapy.Field()
    post_date = scrapy.Field()
