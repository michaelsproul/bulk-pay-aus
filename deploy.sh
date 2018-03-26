#!/bin/bash

set -o errexit
set -o xtrace

host=michael@sproul.xyz

scp -r bulk_pay $host:deploy
scp utils/install.sh $host:deploy

ssh -t $host "sudo bash deploy/install.sh"
