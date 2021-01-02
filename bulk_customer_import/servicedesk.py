import logging

LOG = logging.getLogger(__name__)

class BaseServicedeskManager(object):

    def __init__(self, client):
        self.client = client
        # self.servicedesk_id

    # def get_servicedesk_id(self, project_id_or_key):
    #     # TODO: (simon)
    #     pass

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

        data = {fields[0]: [customer[fields[1]]]}
        response = self.client.post(
            "servicedesk/{}/customer".format(servicedesk),
            data=data,
            experimental=True,
        )

        if response.ok and response.content:
            return response.json()

    def get(self, servicedesk_id):
        pass


class CloudServicedeskManager(BaseServicedesk):

    fields = ("accountIds", "accountId")

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class ServerServicedeskManager(BaseServicedesk):

    fields = ("usernames", "emailAddress")

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
