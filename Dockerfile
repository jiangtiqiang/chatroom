FROM cent6
MAINTAINER erlang tristan.t.jiang@newegg.com
COPY ./* /opt/
CMD chmod +x /opt/start-dev.sh
EXPOSE 8080

