#Build
```
cd ~
hg clone https://bitbucket.org/dpaw/dpaw_ipython/
cd dpaw_ipython
docker build -t "dpaw/ipython" .
```
#Run
```
docker run -p 8888:8888 -v ~/dpaw_ipython/static/home:/home:rw -t -i dpaw/ipython
```
