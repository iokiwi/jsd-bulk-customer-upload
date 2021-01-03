[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)

It's become to much of a burden to maintain this script I no longer personally require.

Atlassian have not made it easy to support both Cloud and server as the products and api's have diverged too significantly.

I have gone deep down a rabit hole of trying to support cloud and server versions but in testing and developing the version of the script currently on master I am no longer sure how well server is and cannot dedicate any more time to this.

# README

A script for bulk uploading organizations and customers to Jira Service desk from a csv file. Aims to solve: [How to Bulk add Organizations and Customers in Service Desk Cloud?](https://community.atlassian.com/t5/Jira-Service-Desk-questions/How-to-Bulk-add-Organizations-and-Customers-in-Service-Desk/qaq-p/85932)

The versions of Jira Service Desk the script has been tested against are.

|Platform|Version|Date Tested|
|---|---|---|
|Service Desk Cloud|`cloud`|`2021-01-04`|
|Service Desk Server|`Not Tested`|`Not Tested`|

## Usage

Requires `python >= 3.5`

```
usage: python -m bulk_customer_import [-h] [-l LOGLEVEL]
                               base_url auth_user auth_pass filename
                               servicedesk_id
```

For example:
```bash
python -m bulk_customer_import \
  "https://mycustomer.atlassian.net" \
  "local-admin" \
  "P4ssw0rd" \
  customers.csv \
  2
```

For help run `python -m bulk_customer_import -h`

The CSV Must Look as follows. See [example.csv](example.csv)
```
Organisation Name,Customer Full Name,Customer Email
ACME,John Snow,john.snow@example.com
Mega Corp,Jane Doe,jane.doe@example.com
Super Company,John Smith,john.smith@example.com
```

Note:
 * There must not be spaces between the `,` and the values
 * The CSV must start with a 'header' row.

## Issues

 * Please include your Jira and Jira Service Desk versions. If you
   are using Cloud just use `cloud` as your version number. For server this information can be found under `Administration` > `Applications` > `Versions and Licenses`.

 * Please copy and paste any error messages which appear in the logs
   when running with the `-l debug` flag. Becareful not to include any
   personally Identifiable information. If you can reproduce the issue
   using the `example.csv` included this repo feel free to use that.

## Contributing

Contributions to this script should work for cloud and the latest version of Jira Service desk.

### Server Development Environment
You can use the docker-compose file included in this repo to spin up a jira service desk server.

```bash
docker-compose up
```

This will start a server on http://localhost:8080/jira. You will need to apply a trial license (for free) and setup the instance. Change the image tag to arget different versions of jira service desk.

Alternatively, you could use the atlassian [SDK](https://developer.atlassian.com/server/framework/atlassian-sdk/)

### Cloud Development Environment
Get a cloud development environment here:
https://blog.developer.atlassian.com/cloud-ecosystem-dev-env/
