import logging

from bulk_customer_import.customer import ServerCustomerManager as CustomerManager 
from bulk_customer_import.organization import ServerOrganizationManager as OrganizationManager
from bulk_customer_import.servicedesk import ServerServicedeskManager as ServerServicedeskManager
from bulk_customer_import.client import BaseClient

LOG = logging.getLogger(__name__)

class ServerClient(BaseClient):

    experimental_api_header = {"X-ExperimentalApi": "opt-in"}

    def __init__(self, *args, **kwargs):

        super().__init__(self, *args, **kwargs)

        self.organization = OrganizationManager(self)
        self.customer = CustomerManager(self)
        self.servicedesk = ServicedeskManager(self)


server_client = None

def get_client(*args, **kwargs):
    global server_client

    if server_client:
        return server_client
    
    server_client = ServerClient(*args, **kwargs)
    return server_client
