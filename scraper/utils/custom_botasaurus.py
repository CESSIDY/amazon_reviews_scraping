# -*- coding: utf-8 -*-
from typing import Callable, Optional
from functools import wraps

from scrapy.utils.project import get_project_settings
from botasaurus import *
import ssl
from cloudscraper import CipherSuiteAdapter


def custom_request(**kwargs):
    settings = get_project_settings()

    def _turn_off_ssl_cert_check(request):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False  # Disable hostname verification
        ssl_context.verify_mode = ssl.CERT_NONE  # Disable certificate verification

        request.ssl_context = ssl_context
        request.mount(
            'https://',
            CipherSuiteAdapter(
                cipherSuite=request.cipherSuite,
                ecdhCurve=request.ecdhCurve,
                server_hostname=request.server_hostname,
                source_address=request.source_address,
                ssl_context=request.ssl_context
            )
        )

    def wrapper(_func: Optional[Callable] = None):
        @request(**kwargs)
        def request_wrapper(request, *args, **kargs):

            # custom logic for turning off ssl cert check
            if not settings.get('SSL_CERT_CHECK_ENABLED'):
                _turn_off_ssl_cert_check(request)

            return _func(request, *args, **kargs)
        return request_wrapper
    return wrapper
