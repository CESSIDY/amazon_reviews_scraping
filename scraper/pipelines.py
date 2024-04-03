from itemadapter import ItemAdapter

from sqlalchemy import Engine, create_engine, cast, Integer
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import insert
from utils.mysql_connection_string import mysql_connection_string

from database.models import Review
from items import ReviewItem


class ReviewsStoringPipeline:
    def __init__(self):
        self.engine: Engine = create_engine(mysql_connection_string())
        self.session = sessionmaker(self.engine)

    def process_item(self, item: ReviewItem, spider):
        with self.session.begin() as session:
            review = {
                "product_code": item.get("product_code"),
                "external_id": item.get("external_id"),
                "review_body": item.get("review_body"),
                "rating_number": item.get("rating_number"),
                "author": item.get("author"),
                "post_date": item.get("post_date"),
            }

            stmt = insert(Review)
            stmt = stmt.on_duplicate_key_update(review).values(review)

            session.execute(stmt)
        return item
