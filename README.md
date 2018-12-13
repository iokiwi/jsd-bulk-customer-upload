# README

[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)

Written to address the need to be able bulk import Customers and Organizations to Jira Service Desk. This was an internal need for my work as an Atlassian Solution partner / Jira Administrator and addressed a need from the community as well.

[How to Bulk add Organizations and Customers in Service Desk Cloud?](https://community.atlassian.com/t5/Jira-Service-Desk-questions/How-to-Bulk-add-Organizations-and-Customers-in-Service-Desk/qaq-p/85932)

It was originally published (by me) as a Gist here -> https://gist.github.com/iokiwi/25f7b5525e8bb542dc44ac1fa02918ef

```
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
```

Currently not really maintained. I am not sure if it is still relevant.

 * Bulk import features may have been added to Atlasssian Cloud Jira Service Desk since this script was written
 * The script used unstable Experimental API end points which may have changed.

Kinda salty that this wasn't the 'accepted solution' for that community post I linked above but whatever - thats just my ego talking.
