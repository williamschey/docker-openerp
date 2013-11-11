# Overview
This is a Docker build script to create a [Docker](http://docker.io) image running [R studio server](http://www.rstudio.com).

The image can be run from within a Linux operating system, providing R studio server running on a specified port.
The image contains as dependencies [Unidata's](http://unidata.ucar.edu/software/netcdf/docs/netcdf-install/Quick-Instructions.html
) HDF5-1.8.11, zlib-1.2.8, and netCDF-4.3.0, as well as texlive-xetex (for [Sweave](http://www.stat.uni-muenchen.de/~leisch/Sweave)).

## Maintainer and License
Maintainer:  Florian Mayer <florian.mayer@dpaw.wa.gov.au>, Department of Parks and Wildlife WA <asi@dpaw.wa.gov.au>
License: [Apache v2](http://www.apache.org/licenses/LICENSE-2.0)

# Usage
## Get the code
```
cd ~
hg clone https://bitbucket.org/dpaw/dpaw_rstudio
```

## Build the image
```
apt-get install docker
cd ~/dpaw_rstudio
docker build -t "dpaw/rstudio" .
```

## Run the image (development)
Choose the IMAGE\_ID of the last successful step in your build.

```
docker run -i -t -entrypoint=bash IMAGE_ID
```

## Run the image (production)
Create a local folder (~/dpaw\_rstudio/static/home) for persistent files of the container and mount it rw through the -v parameter.
Expose R studio server's internal port 8787 to the external port 8787.
Specifically, R studio server will save each user's projects into their home folder.

```
mkdir -p ~/dpaw_rstudio/static/home
docker run -p 8787:8787 -v ~/dpaw_rstudio/static/home:/home/:rw -i -t dpaw/rstudio
```

