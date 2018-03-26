#!/bin/bash

set -o errexit
set -o xtrace

supervisorctl stop bulk_pay

rm -rf ~caddy/apps/bulk-pay-aus/bulk_pay
cp -r deploy/bulk_pay ~caddy/apps/bulk-pay-aus
chown -R caddy:michael ~caddy/apps/bulk-pay-aus/bulk_pay

supervisorctl start bulk_pay
