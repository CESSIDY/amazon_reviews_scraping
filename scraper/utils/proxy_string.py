# -*- coding: utf-8 -*-
from scrapy.utils.project import get_project_settings


def proxy_string() -> str | None:
    """Returns proxy connection string"""
    settings = get_project_settings()
    if not settings.get("PROXY_ENABLED"):
        return None

    proxy = settings.get("PROXY")
    proxy_auth = settings.get("PROXY_AUTH")

    proxy_connection_str = None

    if proxy_auth and proxy:
        proxy_connection_str = "http://{}@{}".format(proxy_auth, proxy)
    elif proxy:
        proxy_connection_str = "http://{}".format(proxy)

    return proxy_connection_str
