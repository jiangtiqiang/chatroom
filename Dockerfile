FROM centos:centos6
MAINTAINER erlang tristan.t.jiang@newegg.com
COPY ./* /project/
RUN setenforce 0
EXPOSE 8080

