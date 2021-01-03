import json
import logging

from urllib.parse import urlparse
from urllib.parse import urljoin

import requests
from requests.auth import HTTPBasicAuth

from bulk_customer_import.servicedesk import CloudServicedeskManager, ServerServicedeskManager # noqa
from bulk_customer_import.customer import CloudCustomerManager, ServerCustomerManager # noqa
from bulk_customer_import.organization import CloudOrganizationManager, ServerOrganizationManager # noqa

LOG = logging.getLogger(__name__)


class BaseClient(object):

    experimental_api_header = None

    def __init__(self, base_url=None, auth_user=None, auth_pass=None,
                 verify=None):

        if not base_url.endswith("/"):
            base_url += "/"
        self.base_url = base_url

        self.verify = verify
        # self.api_url = urljoin(self.base_url)
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
            headers.update({"Content-Type": "application/json"})
            kwargs["data"] = json.dumps(kwargs["data"])

        url = urljoin(self.base_url, url)
        auth = HTTPBasicAuth(self.auth_user, self.auth_pass)

        return requests.request(
            method, url, auth=auth, headers=headers, **kwargs
        )

    def post(self, url, **kwargs):
        headers = kwargs.pop("headers", {})
        headers.update({"Content-Type": "application/json"})
        kwargs["headers"] = headers
        response = self.request("POST", url, **kwargs)
        return response

    def get(self, url, **kwargs):
        response = self.request("GET", url, **kwargs)
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
                LOG.debug("Retrieving resource(s) starting from {}".format(
                    start))
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


class ServerClient(BaseClient):

    experimental_api_header = {"X-ExperimentalApi": "opt-in"}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.organization = ServerOrganizationManager(self)
        self.customer = ServerCustomerManager(self)
        self.servicedesk = ServerServicedeskManager(self)


class CloudClient(BaseClient):

    experimental_api_header = {"X-ExperimentalApi": "true"}

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.organization = CloudOrganizationManager(self)
        self.customer = CloudCustomerManager(self)
        self.servicedesk = CloudServicedeskManager(self)


def get_platform(base_url):

    if urlparse(base_url).netloc.endswith("atlassian.net"):
        return "cloud"
    return "server"


client = None


def get_client(**kwargs):
    global client

    if client:
        return client

    client = {
        "server": ServerClient(**kwargs),
        "cloud": CloudClient(**kwargs)
    }[get_platform(kwargs["base_url"])]

    return client
