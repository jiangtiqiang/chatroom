FROM centos:centos6
MAINTAINER erlang tristan.t.jiang@newegg.com
COPY ./* /usr/
CMD ["/usr/start-dev.sh"]
EXPOSE 8080

