import logging
from requests.exceptions import HTTPError

LOG = logging.getLogger(__name__)


class BaseOrganizationManager(object):

    fields = None

    def __init__(self, client):
        self.client = client

    def list(self):

        LOG.info("Retrieving organizations")
        return self.client.get_paginated_resource(
            "rest/servicedeskapi/organization", "values", experimental=True
        )

    def create(self, name):
        LOG.info("Creating organization")
        return self.client.post(
            "rest/servicedeskapi/organization",
            data={"name": name},
            experimental=True
        ).json()

    def add_customer(self, organization, customer):

        LOG.debug("Adding customer: %s to organization %s" %
                  (customer, organization))

        data = {self.fields[0]: [customer[self.fields[1]]]}

        try:
            response = self.client.post(
                "rest/servicedeskapi/organization/{}/user".format(
                    organization['id']),
                data=data, experimental=True)
            if response.ok and response.content:
                return response.json()
        except HTTPError as e:
            LOG.exception(e)


class CloudOrganizationManager(BaseOrganizationManager):

    # TODO: Remember what this does and make it clear to
    # reader.
    fields = ("accountIds", "accountId")

    def __init__(self, *args):
        super().__init__(*args)

    def add_customer(self, organization, customer):

        if type(customer) == dict:
            customer = self.client.customer.from_dict(customer)

        data = {"accountIds": [customer.get_account_id()]}

        try:
            response = self.client.post(
                "rest/servicedeskapi/organization/{}/user".format(
                    organization['id']),
                data=data, experimental=True)
            if response.ok and response.content:
                return response.json()
        except HTTPError as e:
            LOG.exception(e)


class ServerOrganizationManager(BaseOrganizationManager):

    fields = ("usernames", "emailAddress")

    def __init__(self, *args):
        super().__init__(*args)
