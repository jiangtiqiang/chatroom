FROM centerlang
MAINTAINER erlang tristan.t.jiang@newegg.com
COPY ./* /opt/
RUN yum install -y java
EXPOSE 8080

