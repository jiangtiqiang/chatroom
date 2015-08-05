FROM cent6
MAINTAINER erlang tristan.t.jiang@newegg.com
COPY ./* /opt/
CMD yum install -y java
CMD yum install -y erlang
EXPOSE 8080

