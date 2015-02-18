FROM ubuntu:14.04
MAINTAINER David Rager <drager@medianewsgroup.com>
RUN apt-get update && apt-get install -y pypy wget git
RUN mkdir /pypytmp
RUN mkdir /app
RUN wget -P /pypytmp https://raw.github.com/pypa/pip/master/contrib/get-pip.py
RUN pypy /pypytmp/get-pip.py
RUN rm -rf /pypytmp
RUN /usr/local/bin/pip install tornado
RUN /usr/local/bin/pip install tornado_botocore
RUN /usr/local/bin/pip install pyyaml
RUN git clone https://crania:Violator66@github.com/crania/demo.git /app
EXPOSE 5000
CMD pypy /app/application.py
