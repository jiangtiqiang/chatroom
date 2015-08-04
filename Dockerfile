FROM centos:centos6
MAINTAINER erlang tristan.t.jiang@newegg.com
COPY ./* /project/
RUN su -c "setenforce 0"
EXPOSE 8080

