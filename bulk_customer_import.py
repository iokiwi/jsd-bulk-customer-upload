"""
usage: bulk_customer_import.py [-h] [-l LOGLEVEL]
                               base_url auth_user auth_pass filename
                               servicedesk_id

positional arguments:
  base_url              The url of the hosted instance of JIRA https://yourdomain.atlassian.net
  auth_user             Username for basic http authentication (Account needs to be jira admin)
  auth_pass             Password for basic http authentication
  filename              The filepath to the CSV. CSV is assumed to have a header row. Columns ordered Organisation, Full Name, Email Address
  servicedesk_id        The id of the service desk e.g https://<base_url>/servicedesk/customer/portal/2  <-- the '2' is the ID

optional arguments:
  -h, --help            show this help message and exit
  -l LOGLEVEL, --loglevel LOGLEVEL
                        Set log level (DEBUG,INFO,WARNING,ERROR,CRITICAL)

example:
  python bulk_customer_import.py "https://mycustomer.atlassian.net" "local-admin" "P4ssw0rd" customers.csv 2 -l debug

CSV Format: (CSV is assumed to have a header row)
  Organisation Name, Customer Full Name, Customer Email
  Apple, Steve Jobs, steve.jobs@apple.com
  Microsoft, Bill Gates, bill.gates@microsoft.com
"""

import requests
import json
import logging
import argparse
import csv
import sys

parser = argparse.ArgumentParser()
parser.add_argument("base_url", help="The url of the hosted instance of JIRA")
parser.add_argument("auth_user", help="Username for basic http authentication")
parser.add_argument("auth_pass", help="Password for basic http authentication")
parser.add_argument("filename", help="The name of the csv for bulk upload")
parser.add_argument("servicedesk_id", help="The id of the service desk")
parser.add_argument(
    "-l",
    "--loglevel",
    type=str.upper,
    default="INFO",
    choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    help="Set log level",
)
args = parser.parse_args()

logging.basicConfig(
    level=args.loglevel, format="%(asctime)s - %(levelname)s - %(message)s"
)

jira_session = None
api_url = args.base_url + "/rest/servicedeskapi"

rows_not_processed = []


def init():
    # init session
    global jira_session
    jira_session = get_session(args.base_url, args.auth_user, args.auth_pass)


def parse_csv(filename):
    output = []
    with open(filename, "r") as f:
        reader = csv.reader(f, delimiter=",", quotechar='"')
        for row in reader:
            output.append(row)
    return output


def get_session(base_url, auth_user, auth_pass):
    # init session
    logging.info("Initializing session")
    session = requests.Session()
    session.auth = (auth_user, auth_pass)
    url = base_url + "/rest/auth/1/session"
    response = session.get(url)

    if response.ok:
        return session

    logging.error(
        "Session initialization falied with status {} ({}).".format(
            response.status_code, response.reason
        )
    )
    sys.exit()


def get_paginated_resource(url, content_key, headers=None, params=None):

    if headers is None:
        headers = {}
    if params is None:
        params = {}

    results, last_page, start, step = [], False, 0, 0

    while not last_page:
        params["start"] = start
        response = jira_session.get(url, headers=headers)

        if response.ok:
            _json = json.loads(response.text)
            last_page = _json["isLastPage"]
            start += _json["size"]
            results += _json[content_key]
    return results


def get_organizations():
    headers = {"X-ExperimentalApi": "true"}
    organizations_list = get_paginated_resource(
        api_url + "/organization", "values", headers
    )
    return {
        organization["name"]: organization
        for organization in organizations_list
    }


def add_customer_to_organization(organization, customer):
    headers = {"X-ExperimentalApi": "true", "Content-Type": "application/json"}
    fields = {"accountIds": [customer["accountId"]]}
    url = api_url + "/organization/{}/user".format(organization["id"])
    response = jira_session.post(url, headers=headers, data=json.dumps(fields))

    return response.ok


def add_organization_to_servicedesk(servicedesk_id, organization):
    headers = {"X-ExperimentalApi": "true", "Content-Type": "application/json"}
    fields = {"organizationId": organization["id"]}
    url = api_url + "/servicedesk/{}/organization".format(servicedesk_id)
    response = jira_session.post(url, headers=headers, data=json.dumps(fields))

    if response.ok:
        logging.info(
            "{} was added to service desk {}".format(
                organization["name"], servicedesk_id
            )
        )

    return False


def add_customer_to_servicedesk(servicedesk_id, customer):
    headers = {"X-ExperimentalApi": "true", "Content-Type": "application/json"}
    fields = {"accountIds": [customer["accountId"]]}
    url = api_url + "/servicedesk/{}/customer".format(servicedesk_id)
    response = jira_session.post(url, headers=headers, data=json.dumps(fields))

    if response.ok and response.status_code != 204:
        logging.info(
            "{} was added to service desk {}".format(
                customer["displayName"], servicedesk_id
            )
        )

    return False


def create_customer(customer):
    headers = {"X-ExperimentalApi": "true", "Content-Type": "application/json"}
    payload = {
        "email": customer["emailAddress"],
        "displayName": customer["displayName"],
    }
    url = api_url + "/customer"
    response = jira_session.post(
        url, headers=headers, data=json.dumps(payload)
    )
    logging.debug(response.text)
    if response.ok:
        logging.info(
            "{} was successfully created".format(customer["emailAddress"])
        )
        return json.loads(response.text)

    return False


def create_organization(name):
    headers = {"X-ExperimentalApi": "true", "Content-Type": "application/json"}
    payload = {"name": name}
    url = api_url + "/organization"
    response = jira_session.post(
        url, headers=headers, data=json.dumps(payload)
    )

    if response.ok:
        logging.info("{} was successfully created".format(name))
        return json.loads(response.text)

    return False


def main():
    global rows_not_processed
    # Parse CSV
    rows = parse_csv(args.filename)
    # Get Organisations
    organizations = get_organizations()

    # For each row in the CSV (skip header)
    for row in rows[1:]:
        try:
            organization_name, customer_name, customer_email = (
                row[0],
                row[1],
                row[2],
            )

            # Create the customer if they do not already exist
            new_customer = {
                "displayName": customer_name,
                "emailAddress": customer_email,
            }
            existing_customer = create_customer(new_customer)
            customer = existing_customer if existing_customer else new_customer

            # Create organisation if one does not exist
            if organization_name in organizations.keys():
                organization = organizations[organization_name]
            else:
                organization = create_organization(organization_name)
                add_organization_to_servicedesk(
                    args.servicedesk_id, organization
                )

            # Move the customer into the organization
            add_customer_to_organization(organization, customer)

            # Add the customer into the service desk
            add_customer_to_servicedesk(args.servicedesk_id, customer)
        except Exception as e:
            print("Failed to process row: {}".format(row))
            logging.exception(e)
            rows_not_processed.append(row)

    if rows_not_processed:
        print("An error occurred while processing the following rows.")
        for row in rows_not_processed:
            print(row)


if __name__ == "__main__":
    init()
    main()
