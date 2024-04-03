from typing import Iterable
from datetime import datetime
import logging

import scrapy
from scrapy import Request

from scraper.items import ReviewItem

logger = logging.getLogger(__name__)


class AmazonReviewsSpider(scrapy.Spider):
    name = "amazon_reviews"
    allowed_domains = ["www.amazon.com"]
    product_code = "B01IPHVFUI"
    reviews_url_format_str = "https://www.amazon.com/product-reviews/{code}?filterByStar={rating}&pageNumber={page_number}&language=en_US&sortBy=relevancy&formatType=current_format"
    rating_numbers_to_string_filter = {1: "one_star", 2: "two_star", 3: "three_star", 4: "four_star", 5: "five_star"}

    def start_requests(self) -> Iterable[Request]:
        for rating_number in range(1, 6):
            rating_str = self.rating_numbers_to_string_filter[rating_number]
            yield self.get_next_review_request(rating_str, 1)
        return

    def get_next_review_request(self, rating, next_page_number) -> Request:
        review_url = self.reviews_url_format_str.format(code=self.product_code,
                                                        rating=rating,
                                                        page_number=next_page_number)
        return Request(url=review_url,
                       callback=self.parse_reviews,
                       dont_filter=True,
                       meta={'request_url': review_url},
                       cb_kwargs={"page_number": next_page_number, "rating": rating})

    def parse_reviews(self, response, page_number, rating):
        for review_element in response.xpath("//div[@data-hook='review']"):
            external_id = self._get_external_review_id(review_element)
            review_body = self._get_review_body(review_element)
            rating_number = self._get_review_rating(review_element)
            author = self._get_review_author(review_element)
            post_date = self._get_review_post_date(review_element)

            yield ReviewItem(product_code=self.product_code,
                             external_id=external_id,
                             review_body=review_body,
                             rating_number=rating_number,
                             author=author,
                             post_date=post_date)

        if self._is_last_review_pagination_page(response):
            logger.info(f"Last reviews page. product: {self.product_code} | page: {page_number} | rating: {rating}")
            return

        next_page_number = page_number + 1
        yield self.get_next_review_request(rating, next_page_number)

    @staticmethod
    def _get_external_review_id(review_element):
        return review_element.xpath("./@id").get()

    @staticmethod
    def _get_review_body(review_element):
        return review_element.xpath(".//*[contains(@data-hook, 'review-body')]/span").get()

    @staticmethod
    def _get_review_rating(review_element):
        xpath = ".//i[contains(@data-hook, 'review-star-rating') and contains(@class, 'a-star-')]/@class"
        rating_str = review_element.xpath(xpath).re_first(r'a-star-(\d+)', default='0')
        return float(rating_str)

    @staticmethod
    def _get_review_author(review_element):
        return review_element.xpath(".//*[@class='a-profile-name']/text()").get()

    @staticmethod
    def _get_review_post_date(review_element):
        raw_post_date_str: str = review_element.xpath(".//*[@data-hook='review-date']/text()").get()
        raw_post_date_str = raw_post_date_str.replace(",", "").replace(".", "")
        date_str = " ".join(raw_post_date_str.split(" ")[-3:])
        return datetime.strptime(date_str, "%B %d %Y").date()

    @staticmethod
    def _is_last_review_pagination_page(response) -> bool:
        return not response.xpath("//li[contains(@class, 'a-last') and not(contains(@class, 'a-disabled'))]")
