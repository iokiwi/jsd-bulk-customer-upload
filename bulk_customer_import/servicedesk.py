import logging

LOG = logging.getLogger(__name__)


class ServicedeskManager(object):
    def __init__(self, client):
        self.client = client

    def add_organization(self, servicedesk, organization):

        LOG.info("Adding organization to service desk")

        response = self.client.post(
            "servicedesk/{}/organization".format(servicedesk),
            data={"organizationId": organization["id"]},
            experimental=True,
        )

        if response.ok and response.content:
            return response.json()

    def add_customer(self, servicedesk, customer):

        LOG.info("Adding customers to service desk")

        # TODO(Simon): to do confirm if this is correct for server
        fields = ("usernames", "emailAddress")
        if self.client.platform == "cloud":
            fields = ("accountIds", "accountId")
        data = {fields[0]: [customer[fields[1]]]}

        response = self.client.post(
            "servicedesk/{}/customer".format(servicedesk),
            data=data,
            experimental=True,
        )

        if response.ok and response.content:
            return response.json()
