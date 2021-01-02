import json
import logging

from urllib.parse import urlparse
from urllib.parse import urljoin

import requests
from requests.auth import HTTPBasicAuth

from bulk_customer_import.client import ServerClient
from bulk_customer_import.client import CloudClient

LOG = logging.getLogger(__name__)


class BaseClient(object):

    experimental_api_header = None

    def __init__(self, base_url=None, auth_user=None, auth_pass=None,
                 verify=None, **kwargs):
        if not base_url.endswith("/"):
            base_url += "/"
        self.base_url = base_url
        self.verify = verify
        self.api_url = urljoin(self.base_url, "rest/servicedeskapi/")
        self.auth_pass = auth_pass
        self.auth_user = auth_user
        self.organization = None
        self.servicedesk = None
        self.customer = None

    def request(self, method, url, verify=True, experimental=False, **kwargs):

        headers = kwargs.pop("headers", {})

        if experimental:
            headers.update(self.experimental_api_header)

        if "data" in kwargs:
            kwargs["data"] = json.dumps(kwargs["data"])

        url = urljoin(self.api_url, url)
        auth = HTTPBasicAuth(self.auth_user, self.auth_pass)

        return requests.request(
            method, url, auth=auth, headers=headers, **kwargs
        )

    def post(self, url, **kwargs):
        headers = kwargs.pop("headers", {})
        headers.update({"Content-Type": "application/json"})
        kwargs["headers"] = headers
        response = self.request("POST", url, **kwargs)

        if not response.ok:
            LOG.debug(response.text)

        response.raise_for_status()
        return response

    def get(self, url, **kwargs):
        response = self.request("GET", url, **kwargs)
        response.raise_for_status()

        if not response.ok:
            LOG.debug(response.text)

        return response

    def get_paginated_resource(self, url, content_key, **kwargs):

        LOG.info("Retrieving all resources from paginated endpoint."
                 "this may take a while")

        results = []
        last_page = False
        start = 0
        size = None

        params = kwargs.get("params", {})
        while not last_page:
            if size:
                LOG.debug("Retrieving next {} resource(s) {} - {}".format(
                         size, start, start+size))
            else:
                LOG.debug("Retrieving resource(s) starting from {}"
                         .format(start))
            params["start"] = start
            LOG.debug("request params: {}".format(params))
            response = self.get(url, params=params, **kwargs).json()
            LOG.debug(response)
            last_page = response["isLastPage"]
            size = response["size"]
            start += size
            results += response[content_key]
        return results

    def __str__(self):
        details = {
            "verify": self.verify,
            "base_url": self.base_url}
        return "Client {}".format(details)


def get_platform(base_url):
    if urlparse(self.base_url).netloc.endswith("atlassian.net"):
        return "cloud"
    return "server"

client = None

def get_client(*args, **kwargs):
    global client

    if client:
        return client

    return {
        "server": ServerClient(*args, **kwargs)
        "cloud": CloudClient(*args, **kwargs)
    }[get_platform(kwargs["base_url"])]

