#!/bin/sh
exec erl \
    -pa /opt/ebin /opt/deps/*/ebin \
    -boot start_sasl \
    -sname chatroom_dev \
    -s chatroom \
    -s reloader
