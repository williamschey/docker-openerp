#!/bin/bash
docker run -t -i -p 8223:8080 -v `pwd`/persist/var/lib/postgresql:/var/lib/postgresql -v `pwd`/persist/var/local/jira:/var/local/jira docker.dpaw.wa.gov.au/jira:6.1.2 "$@"
