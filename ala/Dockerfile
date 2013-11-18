# Provides R, R studio server + Latex + netCDF, HDF5, zlib
FROM docker.dpaw.wa.gov.au/ubuntu:12.04
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

#RUN wget http://download2.rstudio.org/rstudio-server-0.97.551-amd64.deb
#RUN dpkg-divert --local --rename --add /sbin/initctl; ln -s /bin/true /sbin/initctl;
#RUN dpkg -i rstudio-server-0.97.551-amd64.deb
# after install, these directories are missing:
#RUN mkdir -p /var/run/rstudio-server /var/lock/rstudio-server /var/log/rstudio-server \ 
# /var/lib/rstudio-server/conf /var/lib/rstudio-server/body /var/lib/rstudio-server/proxy

# apparmor
#RUN cp /usr/lib/rstudio-server/extras/apparmor/rstudio-server /etc/apparmor.d/
#RUN apparmor_parser -r /etc/apparmor.d/rstudio-server ## apparmor_parser: not found

ENTRYPOINT ["sh", "-c", "bash"]
#EXPOSE 8787

