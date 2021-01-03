import logging

LOG = logging.getLogger(__name__)


class BaseServicedeskManager(object):

    fields = None

    def __init__(self, client):
        self.client = client

    def add_organization(self, servicedesk, organization):

        LOG.info("Adding organization to service desk")

        response = self.client.post(
            "rest/servicedeskapi/servicedesk/{}/organization".format(
                servicedesk),
            data={"organizationId": organization["id"]},
            experimental=True,
        )

        if response.ok and response.content:
            return response.json()

    def add_customer(self, servicedesk, customer):

        LOG.info("Adding customer to service desk: %s" % customer)

        data = {self.fields[0]: [customer[self.fields[1]]]}
        LOG.debug(data)
        response = self.client.post(
            "rest/servicedeskapi/servicedesk/{}/customer".format(servicedesk),
            data=data,
            experimental=True,
        )

        if response.ok and response.content:
            return response.json()

    def get(self, servicedesk_id):
        pass


class CloudServicedeskManager(BaseServicedeskManager):

    fields = ("accountIds", "accountId")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_customer(self, servicedesk, customer):

        if type(customer) == dict:
            customer = self.client.customer.from_dict(customer)

        LOG.info("Adding customer to service desk: %s" % customer)

        account_id = customer.get_account_id()

        response = self.client.post(
            "rest/servicedeskapi/servicedesk/{}/customer".format(servicedesk),
            data={"accountIds": [account_id]},
            experimental=True,
        )

        if response.ok and response.content:
            return response.json()


class ServerServicedeskManager(BaseServicedeskManager):

    fields = ("usernames", "emailAddress")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
