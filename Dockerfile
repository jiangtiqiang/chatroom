FROM slave/tomcat
MAINTAINER erlang tristan.t.jiang@newegg.com
COPY ./* /project/
EXPOSE 8080

