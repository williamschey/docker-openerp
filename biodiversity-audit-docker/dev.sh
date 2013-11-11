#!/bin/bash
docker run -p 8080 -t -i -v `pwd`/../persist/var/lib/postgresql:/var/lib/postgresql -v `pwd`/../persist/opt/biodiversity-audit/src:/opt/biodiversity-audit/src bio "$@"
