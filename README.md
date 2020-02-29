# README

Hey! This is bought to you for free under the GPL3 license. If it helped you, please consider supporting this project by contributing, sharing it far and wide and/or making a small donation.

<a href='https://ko-fi.com/K3K21GRP3' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://az743702.vo.msecnd.net/cdn/kofi4.png?v=2' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

A script for bulk uploading organizations and customers to Jira Service desk from a csv file. Aims to solve: [How to Bulk add Organizations and Customers in Service Desk Cloud?](https://community.atlassian.com/t5/Jira-Service-Desk-questions/How-to-Bulk-add-Organizations-and-Customers-in-Service-Desk/qaq-p/85932)

The versions of Jira Service Desk the script has been tested against are.

|Platform|Version|Date Tested|
|---|---|---|
|Service Desk Cloud|`cloud`|`2020-02-27`|
|Service Desk Server|`4.7.1`|`2020-02-29`|

## Usage
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

The CSV Must Look as follows
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

This will start a server on http://localhost:8080. You will need to apply a trial license and setup the instance. Change the image tag to arget different versions of jira service desk.

Alternatively, you could use the atlassian [SDK](https://developer.atlassian.com/server/framework/atlassian-sdk/)

### Cloud Development Environment
Get a cloud development environment here:
https://blog.developer.atlassian.com/cloud-ecosystem-dev-env/
