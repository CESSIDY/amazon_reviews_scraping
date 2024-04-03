import scrapy


class ReviewItem(scrapy.Item):
    review_body = scrapy.Field()
    rating_number = scrapy.Field()
    author = scrapy.Field()
    post_date = scrapy.Field()
