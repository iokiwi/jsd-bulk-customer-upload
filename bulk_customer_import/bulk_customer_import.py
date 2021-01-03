import logging
import argparse

from client.base import get_client
from bulk_customer_import import utils

parser = argparse.ArgumentParser()
parser.add_argument(
    "base_url",
    help="The url of the hosted instance of JIRA")
parser.add_argument(
    "auth_user",
    help="Username for basic http authentication")
parser.add_argument(
    "auth_pass",
    help="Password for basic http authentication")
parser.add_argument(
    "filename",
    help="The name of the csv for bulk upload")
parser.add_argument(
    "servicedesk_id",
    help="The id of the service desk")
parser.add_argument(
    "--verify",
    choices=["True", "False"],
    default="True",
    type=bool,
    help="Verify the ssl certificate")
parser.add_argument(
    "-l",
    "--loglevel",
    type=str.upper,
    default="ERROR",
    choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    help="Set log level",
)
args = parser.parse_args()

logging.basicConfig(
    level=args.loglevel,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

LOG = logging.getLogger(__name__)


def main():

    client = get_client(
        base_url=args.base_url,
        auth_user=args.auth_user,
        auth_pass=args.auth_pass)
    LOG.debug(client)

    servicedesk_id = args.servicedesk_id
    # Parse CSV
    rows = utils.parse_csv(args.filename)
    # Get Organisations
    organizations = client.organization.list()

    organizations = {organization["name"]: organization
                     for organization in organizations}

    # For each row in the CSV (skip header)
    rows_not_processed = []
    rows = rows[1:]

    total_rows = len(rows)
    row_num = 0

    for row in rows:
        row_num += 1
        print("[{}/{}] Processing row: {}".format(
            row_num, total_rows, row
        ))

        try:
            organization_name, customer_name, customer_email = (
                row[0],
                row[1],
                row[2],
            )

            if customer_email and customer_name:

                print("Creating customer:")
                print("Name:", customer_name)
                print("Email", customer_email)

                customer = client.customer.create(
                    customer_name, customer_email
                )

                print("Adding {} to the service desk".format(customer.email))
                client.servicedesk.add_customer(
                    servicedesk_id, customer.to_dict())

            if organization_name:
                # Create organization if one does not exist
                if organization_name in organizations:
                    print("Organization already exists: {}".format(
                        organization_name))
                    organization = organizations[organization_name]
                else:
                    print("Creating Organization: {}".format(
                        organization_name))
                    organization = client.organization.create(
                        organization_name)

                # To do, this should be abstracted
                client.servicedesk.add_organization(
                    args.servicedesk_id, organization)

                LOG.info("Organization already part of service desk")

            if customer_name and customer_email and organization_name:
                # Move the customer into the organization
                client.organization.add_customer(
                    organization, customer.to_dict())

        except Exception as e:  # noqa
            LOG.exception("Failed to process row: {}".format(row))
            rows_not_processed.append(row)

    if rows_not_processed:
        print("An error occurred while processing the following rows.")
        for row in rows_not_processed:
            print(row)
