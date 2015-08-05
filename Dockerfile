FROM cent6
MAINTAINER erlang tristan.t.jiang@newegg.com
COPY ./* /opt/
CMD yum install erlang
EXPOSE 8080

