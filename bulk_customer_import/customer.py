import logging

LOG = logging.getLogger(__name__)


class BaseCustomerManager(object):

    def __init__(self, client):
        self.client = client

    def _create(self, customer):
        # Try create customer

        response = self.client.post(
            "rest/servicedeskapi/customer",
            data=customer.to_dict(),
            experimental=True)

        if response.ok:
            customer = self.from_dict(response.json())
            return customer

        try:
            print(response.json()["i18nErrorMessage"]["parameters"])
        except KeyError:
            LOG.error(response.text)

        return customer

    def search(self):
        raise ("Not Implemented")


class ServerCustomerManager(BaseCustomerManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(self, name, email):
        customer = ServerCustomer(name, email)
        return self._create(customer)

    def find(self, value, field="email"):
        response = self.client.get(
            "rest/api/2/user/search",
            params={"username": value})
        response.raise_for_status()

        results = response.json()

        for result in results:
            if result[field] == value:
                return self.from_dict(result)

    def from_dict(self, data):
        return ServerCustomer(
            name=data["fullName"],
            email=data["email"],
            client=self.client,
        )


class CloudCustomerManager(BaseCustomerManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, customer):
        data = {
            "displayName": customer.name,
            "email": customer.email
        }
        response = self.client.post(
            "rest/servicedeskapi/customer",
            data=data, experimental=True)

        if response.ok:
            return self.from_dict(response.json())

        try:
            print(response.json()["i18nErrorMessage"]["parameters"])
        except KeyError:
            LOG.debug(response.text)

        return customer

    def create(self, name=None, email=None):
        customer = CloudCustomer(name=name, email=email)
        return self._create(customer)

    def find(self, value, field="emailAddress"):
        response = self.client.get(
            "rest/api/latest/user/search",
            params={"query": value},)

        if not response.ok:
            LOG.debug(response.text)

        results = response.json()
        LOG.debug(results)
        for result in results:
            if result[field] == value:
                return CloudCustomer(
                    name=result["displayName"],
                    email=result["emailAddress"],
                    account_id=result["accountId"],
                    client=self.client
                )
        return None

    def from_dict(self, data):
        LOG.debug("Deserialzing customer from dict: %s" % data)
        return CloudCustomer(
            account_id=data.get("accountId"),
            name=data.get("displayName"),
            # TODO check email vs email address for search
            email=data.get("email"),
            client=self.client,
        )


class BaseCustomer(object):

    def __init__(self, name=None, email=None, client=None):
        self.name = name
        self.email = email
        self.client = client

    def __str__(self):
        return "<Customer name: {}, email: {}, client: {}>".format(
            self.name, self.email, self.client
        )


class CloudCustomer(BaseCustomer):

    def __init__(self, account_id=None, **kwargs):
        super().__init__(**kwargs)
        self.account_id = account_id

    def get_account_id(self):
        if self.account_id:
            return self.account_id

        customer = self.client.customer.find(self.email)
        self.account_id = customer.account_id
        return self.account_id

    def to_dict(self):
        return {
            "accountId": self.account_id,
            "displayName": self.name,
            "email": self.email
        }

    def __str__(self):
        msg = "<Customer name: {}, email: {}, accountId; {}, client: {}>"
        return msg.format(
            self.name, self.email, self.account_id, self.client
        )


class ServerCustomer(BaseCustomer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dict(self):
        return {
            "fullName": self.name,
            "email": self.email
        }
