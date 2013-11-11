# Yes You CKAN!
Yes You CKAN is an open source [Fabric](http://docs.fabfile.org/en/1.8/) script to install the data catalog [CKAN](http://ckan.org/) 
with the plugins [filestore](http://docs.ckan.org/en/latest/filestore.html), [datastore](http://docs.ckan.org/en/latest/datastore.html), 
[ckanext-spatial](https://github.com/okfn/ckanext-spatial) and [harvest](https://github.com/okfn/ckanext-harvest/) 
in a [Ubuntu 12.04 LTS](http://releases.ubuntu.com/precise/) environment with a few deployment customisations.

Warning: This is work in progress, some things might work not yet as expected, so proceed with caution.

# Whom to blame
Yes You CKAN was commissioned, and is maintained, by the Marine Science Program of the [Western Australian Department of Parks and Wildlife](http://www.dpaw.wa.gov.au/) 
and developed with [Gaia Resources](http://www.gaiaresources.com.au/website/gaiaresources/).

Copyright 2013 Department of Parks & Wildlife

Licensed under the Apache License, Version 2.0 (the “License”); you may not use this file except in compliance with the License. 
You may obtain a copy of the License at [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0).
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an “AS IS” BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing 
permissions and limitations under the License.

## Main Contributors
 * [Anthony Jones](mailto:Anthony@gaiaresources.com.au), Gaia Resources
 * [Florian Mayer](mailto:Florian.Mayer@dpaw.wa.gov.au), DPaW

# Why customise the deployment?
CKAN's own deployment recipe is perfectly fine. While the default install sets up CKAN globally, 
this deployment allows for [custom installation directories](https://bitbucket.org/dpaw/yes_you_ckan/wiki/Custom%20local%20settings), 
host ports, and database settings. It also automates the upload of an initial set of organizations, groups, users, etc.

See full installation instructions [on our Wiki](https://bitbucket.org/dpaw/yes_you_ckan/wiki/Home).
