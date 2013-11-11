# Current install errors:
The following packages have unmet dependencies:
 r-base-core : Depends: libblas3 but it is not installable or
                        libblas.so.3 but it is not installable or
                        libatlas3-base but it is not installable
               Depends: libc6 (>= 2.16) but 2.15-0ubuntu10 is to be installed
               Depends: liblapack3 but it is not installable or
                        liblapack.so.3 but it is not installable or
                        libatlas3-base but it is not installable
               Depends: liblzma5 (>= 5.1.1alpha+20120614) but 5.1.1alpha+20110809-3 is to be installed
               Depends: libtiff5 (> 4.0.0-1~) but it is not installable
               Recommends: r-base-dev but it is not going to be installed
 r-recommended : Depends: r-cran-kernsmooth (>= 2.2.14) but it is not going to be installed
                 Depends: r-cran-mgcv (>= 1.1.5) but it is not going to be installed
                 Depends: r-cran-matrix but it is not going to be installed
E: Unable to correct problems, you have held broken packages.
Error build: The command [/bin/sh -c apt-get install -y r-base-core r-recommended r-base-html r-base] returned a non-zero code: 255

