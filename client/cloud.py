import logging

from bulk_customer_import.customer import CloudCustomerManager as CustomerManager
from bulk_customer_import.organization import CloudOrganizationManager as OrganizationManager
from bulk_customer_import.servicedesk import CloudServicedeskManager as CloudServicedeskManager
from bulk_customer_import.client import BaseClient

LOG = logging.getLogger(__name__)

class CloudClient(BaseClient):

    experimental_api_header = {"X-ExperimentalApi": "true"}

    def __init__(self, *args, **kwargs):

        super().__init__(self, *args, **kwargs)

        self.organization = OrganizationManager(self)
        self.customer = CustomerManager(self)
        self.servicedesk = ServicedeskManager(self)

cloud_client = None

def get_client(*args, **kwargs):
    global cloud_client

    if cloud_client:
        return cloud_client

    cloud_client = CloudClient(*args, **kwargs)
    return cloud_cleint
