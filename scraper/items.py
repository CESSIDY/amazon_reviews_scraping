from datetime import datetime

import scrapy


class ReviewItem(scrapy.Item):
    product_code = scrapy.Field()
    external_id = scrapy.Field()

    review_body = scrapy.Field()
    rating_number = scrapy.Field()
    author = scrapy.Field()
    post_date = scrapy.Field()

    def to_dict(self):
        return {
            "product_code": self.get("product_code"),
            "external_id": self.get("external_id"),
            "review_body": self.get("review_body"),
            "rating_number": self.get("rating_number"),
            "author": self.get("author"),
            "post_date": self.get("post_date").strftime("%Y-%m-%d"),
        }

    def from_dict(self, data):
        self['product_code'] = data.get("product_code"),
        self['external_id'] = data.get("external_id"),
        self['review_body'] = data.get("review_body"),
        self['rating_number'] = data.get("rating_number"),
        self['author'] = data.get("author"),
        self['post_date'] = datetime.strptime(data.get("post_date"), "%Y-%m-%d").date(),
