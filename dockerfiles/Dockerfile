FROM ubuntu:14.04
MAINTAINER David Rager <drager@medianewsgroup.com>
RUN apt-get update && apt-get install -y pypy wget git
RUN mkdir /pypytmp
RUN wget -P /pypytmp https://raw.github.com/pypa/pip/master/contrib/get-pip.py
RUN pypy /pypytmp/get-pip.py
RUN rm -rf /pypytmp
RUN /usr/local/bin/pip install tornado
RUN /usr/local/bin/pip install tornado_botocore
RUN /usr/local/bin/pip install pyyaml

EXPOSE 80
