import logging

LOG = logging.getLogger(__name__)

class BaseCustomerManager(object):

    # name_field_key = None
    customer_class = None

    def __init__(self, client):
        self.client = client

    def create(self, name, email):

        LOG.info("Creating customer")

        self.customer_class(name, email)

        response = self.client.post(
            "customer", data=customer.to_dict(), experimental=True)

        # TODO: Handle if customer already exists

        customer = self.customer_class.from_dict(response.json())

        return customer

    def from_dict(self, d):
        return {
            self.name_field_key: self.name,
            "email": self.email
        }


def BaseCustomer(object):

    name_field_key = None

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def to_dict(self):
        return {
            self.name_field_key: self.name,
            "email": self.email
        }

class CloudCustomer(BaseCustomer):

    name_field_key = "displayName"

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    # def to_dict(self):
    #     return {
    #         "displayName": self.name,
    #         "email": self.email
    #     }


class ServerCustomer(BaseCustomer):

    name_field_key = "fullName"

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    # def to_dict(self):
    #     return {
    #         "fullName": self.name,
    #         "email": self.email
    #     }


class ServerCustomerManager(BaseCustomerManager):

    customer_class = ServerCustomer

    def __init__(self):
        super().__init__(self, *args, **kwargs)


class CloudCustomerManager(BaseCustomerManager):

    customer_class = CloudCustomer

    def __init__(self):
        super().__init__(self, *args, **kwargs)
