import logging

LOG = logging.getLogger(__name__)


class CustomerManager(object):
    def __init__(self, client):
        self.client = client

    def create(self, name, email):

        LOG.info("Creating customer")

        name_field_key = "fullName"
        if self.client.platform == "cloud":
            name_field_key = "displayName"

        customer = {"email": email, name_field_key: name}
        response = self.client.post(
            "customer", data=customer, experimental=True)
        return response.json()
