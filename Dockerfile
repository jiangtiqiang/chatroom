FROM slave/tomcat
MAINTAINER erlang tristan.t.jiang@newegg.com
COPY ./* /opt/
EXPOSE 8080

