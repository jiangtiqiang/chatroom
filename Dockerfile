FROM cent6
MAINTAINER erlang tristan.t.jiang@newegg.com
COPY ./* /opt/
RUN yum install -y java
RUN yum remove -y erlang
EXPOSE 8080

