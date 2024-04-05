import json
from typing import Iterable
from datetime import datetime
import logging
from requests.models import Response
import os

import scrapy
from scrapy.http import HtmlResponse
from botasaurus import *
from botasaurus.create_stealth_driver import create_stealth_driver

from scraper.utils import proxy_string, custom_request
from scraper.items import ReviewItem

logger = logging.getLogger(__name__)


class AmazonReviewsBotasaurusRequestSpider(scrapy.Spider):
    name = "amazon_reviews_botasaurus_request"
    allowed_domains = ["www.amazon.com"]
    start_urls = ["https://www.amazon.com"]
    product_code = "B01IPHVFUI"
    reviews_url_format_str = "https://www.amazon.com/product-reviews/{code}?filterByStar={rating}&pageNumber={page_number}&language=en_US&sortBy=relevancy&formatType=current_format"
    rating_numbers_to_string_filter = {1: "one_star", 2: "two_star", 3: "three_star", 4: "four_star", 5: "five_star"}
    MAX_PAGE_LIMIT = 10

    def parse(self, response):
        reviews_scraper_queue = AmazonReviewsBotasaurusRequestSpider.scrape_reviews_task()
        for rating_number in range(1, 2):  # TODO: Change to 6
            rating_filter = self.rating_numbers_to_string_filter[rating_number]
            reviews_scraper_queue.put({'self': self, 'rating_filter': rating_filter})
        reviews = reviews_scraper_queue.get()

        for review in reviews:
            yield ReviewItem().from_dict(json.loads(review))

    @staticmethod
    @custom_request(async_queue=True, proxy=proxy_string())
    def scrape_reviews_task(request: AntiDetectRequests, data):
        all_reviews = []
        for page_number in range(1, data['self'].MAX_PAGE_LIMIT + 1):
            response = data['self'].make_next_review_request(request, data['rating_filter'], page_number)
            reviews = data['self'].parse_reviews(response)
            all_reviews.extend(reviews)
            if data['self']._is_last_review_pagination_page(response):
                logger.info(
                    f"Last reviews page. product: {data['self'].product_code} | page: {page_number} | rating: {data['rating_filter']}")
                return all_reviews
        return all_reviews

    def make_next_review_request(self, request: AntiDetectRequests, rating, next_page_number) -> HtmlResponse:
        review_url = self.reviews_url_format_str.format(code=self.product_code,
                                                        rating=rating,
                                                        page_number=next_page_number)
        response = request.get(review_url, verify=True if self.settings['SSL_CERT_CHECK_ENABLED'] else None)
        return HtmlResponse(
            url=review_url,
            body=response.text,
            encoding='utf-8',
            status=response.status_code,
        )

    def parse_reviews(self, response: HtmlResponse):
        reviews = []
        for review_element in response.xpath("//div[@data-hook='review']"):
            external_id = self._get_external_review_id(review_element)
            review_body = self._get_review_body(review_element)
            rating_number = self._get_review_rating(review_element)
            author = self._get_review_author(review_element)
            post_date = self._get_review_post_date(review_element)

            review = ReviewItem(product_code=self.product_code,
                                external_id=external_id,
                                review_body=review_body,
                                rating_number=rating_number,
                                author=author,
                                post_date=post_date)
            reviews.append(json.dumps(review.to_dict()))
        return reviews

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
    def _is_last_review_pagination_page(response: HtmlResponse) -> bool:
        return not response.xpath("//li[contains(@class, 'a-last') and not(contains(@class, 'a-disabled'))]")
