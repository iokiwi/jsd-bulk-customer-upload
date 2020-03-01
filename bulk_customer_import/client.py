import json
import logging

from urllib.parse import urlparse
from urllib.parse import urljoin

import requests
from requests.auth import HTTPBasicAuth

from bulk_customer_import.customer import CustomerManager
from bulk_customer_import.organization import OrganizationManager
from bulk_customer_import.servicedesk import ServicedeskManager


LOG = logging.getLogger(__name__)


class Client(object):
    def __init__(self, base_url=None, auth_user=None, auth_pass=None,
                 verify=None, **kwargs):
        if not base_url.endswith("/"):
            base_url += "/"
        self.base_url = base_url
        self.verify = verify
        self.api_url = urljoin(self.base_url, "rest/servicedeskapi/")
        self.auth_pass = auth_pass
        self.auth_user = auth_user
        self.organization = OrganizationManager(self)
        self.customer = CustomerManager(self)
        self.servicedesk = ServicedeskManager(self)

    def request(self, method, url, verify=True, experimental=False, **kwargs):

        headers = kwargs.pop("headers", {})
        if experimental and self.platform == "server":
            headers.update({"X-ExperimentalApi": "opt-in"})
        if experimental and self.platform == "cloud":
            headers.update({"X-ExperimentalApi": "true"})

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

        results, last_page, start = [], False, 0
        params = kwargs.get("params", {})
        while not last_page:
            params["start"] = start
            response = self.get(url, **kwargs).json()
            last_page = response["isLastPage"]
            start += response["size"]
            results += response[content_key]

        return results

    @property
    def platform(self):
        if urlparse(self.base_url).netloc.endswith("atlassian.net"):
            return "cloud"
        return "server"

    def __str__(self):
        details = {
            "platform": self.platform,
            "verify": self.verify,
            "base_url": self.base_url}
        return "Client {}".format(details)


client = None


def get_client(*args, **kwargs):
    global client
    if client:
        return client
    return Client(*args, **kwargs)
