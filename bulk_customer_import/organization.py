import logging

LOG = logging.getLogger(__name__)


class OrganizationManager(object):
    def __init__(self, client):
        self.client = client

    def list(self):
        LOG.info("Retrieving organisations")
        return self.client.get_paginated_resource(
            "organization", "values", experimental=True
        )

    def create(self, name):
        LOG.info(f"Creating organisation")
        return self.client.post(
            "organization", data={"name": name}, experimental=True
        ).json()

    def add_customer(self, organization, customer):
        LOG.info(f"Adding customer to organization")
        # TODO(Simon): to do confirm if this is correct for server
        fields = ("usernames", "emailAddress")
        if self.client.platform == "cloud":
            fields = ("accountIds", "accountId")
        data = {fields[0]: [customer[fields[1]]]}

        response = self.client.post(
            f"organization/{organization['id']}/user",
            data=data, experimental=True)

        if response.ok and response.content:
            return response.json()
