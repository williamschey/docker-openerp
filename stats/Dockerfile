# NOTE: Docker currently has a bug where images built with ENV commands
# and included with FROM force a cache miss. This gets really annoying.
# See https://github.com/dotcloud/docker/issues/1903
#FROM dpaw/postgresql:9.3
# Provides R, R studio server + Latex + netCDF, HDF5, zlib

FROM dpaw/ubuntu
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

##### Begin R block.
ENV HOMEDIR /var/www/stats
RUN mkdir -p $HOMEDIR && cd $HOMEDIR
RUN echo deb http://cran.csiro.au/bin/linux/ubuntu raring/ >> /etc/apt/sources.list
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9
#RUN add-apt-repository ppa:marutter/rdev
RUN apt-get update
RUN apt-get upgrade
RUN apt-get install -f
RUN apt-get install -y libcurl4-openssl-dev gdebi-core libapparmor1 wget git-core
RUN apt-get install -y r-base-core r-recommended r-base-html r-base 
RUN wget http://download2.rstudio.org/rstudio-server-0.97.551-amd64.deb
RUN gdebi rstudio-server-0.97.551-amd64.deb 
##### End R block.

##### Begin netCDF block.
RUN wget zlib.net/zlib-1.2.8.tar.gz && tar -xvzf wget zlib-1.2.8.tar.gz
RUN wget http://www.hdfgroup.org/ftp/HDF5/current/src/hdf5-1.8.11.tar.bz2 && tar -xvzf hdf5-1.8.11.tar.bz2
RUN wget http://www.unidata.ucar.edu/downloads/netcdf/ftp/netcdf-4.3.0.tar.gz && tar -xvzf netcdf-4.3.0.tar.gz

RUN cd $HOMEDIR/zlib-1.2.8/ && ./configure && make && make install
RUN cd $HOMEDIR/hdf5-1.8.11 && ./configure && make && make install
RUN cd $HOMEDIR/netcdf-4.3.0 && ./configure && make && make install
##### End netCDF block.

##### Begin latex block.
RUN sudo apt-get install -y texlive-xetex
##### End latex block.

# RUN ECHO my content lines > /etc/my/file.conf
ENTRYPOINT ["startup.py"]
