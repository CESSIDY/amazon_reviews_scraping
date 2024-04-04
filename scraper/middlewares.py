# -*- coding: utf-8 -*-
import logging

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from scrapy import Request, Spider
from w3lib.http import basic_auth_header


class CustomRetryMiddleware(RetryMiddleware):
    logger = logging.getLogger(__name__.split('.')[-1])

    def process_response(self, request, response, spider):
        if request.meta.get("dont_retry", False):
            return
        if response.selector.type not in ("html", "xml", "text"):
            self.logger.warning("Incorrect response type received")
            return response

        if self._is_redirected_at_login_page(response):
            reason = "Redirected to login"
            request = request.replace(url=request.meta.get("request_url", request.url))
            return self._retry(request, reason, spider) or response
        elif self._is_captcha_page(response):
            reason = "Received captcha"
            return self._retry(request, reason, spider) or response
        elif self._is_retry_status(response):
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response

    def _is_retry_status(self, response):
        return bool(response.status in self.retry_http_codes)

    @staticmethod
    def _is_last_retry(request):
        retry_times = request.meta.get("retry_times", 0)
        max_retry_times = request.meta.get("max_retry_times", 0)
        return bool(retry_times == max_retry_times)

    @staticmethod
    def _is_redirected_at_login_page(response):
        return bool("www.amazon.com/ap/signin" in response.url)

    @staticmethod
    def _is_captcha_page(response):
        return response.xpath("//form[contains(@action, 'Captcha')]")


class HttpProxyMiddleware:
    logging_enabled = True

    @staticmethod
    def update_request(request: Request, spider: Spider) -> Request:
        if "proxy" not in request.meta.keys():
            proxy = spider.settings.get("PROXY")
            proxy_auth = spider.settings.get("PROXY_AUTH")

            if not proxy:
                raise Exception("Proxy enabled but not configured")

            if proxy_auth:
                request.headers["Proxy-Authorization"] = basic_auth_header(*proxy_auth.split(":"))
            if "http" not in proxy:
                proxy = "http://{}".format(proxy)
            request.meta["proxy"] = proxy
            return request

    def process_request(self, request: Request, spider: Spider) -> None:
        if hasattr(spider, "proxy_enabled") and spider.proxy_enabled or spider.settings.get("PROXY_ENABLED"):
            request = HttpProxyMiddleware.update_request(request, spider)
        else:
            if self.logging_enabled:
                spider.logger.warning("PROXY DISABLED")
                self.logging_enabled = False
