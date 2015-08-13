#!/bin/sh
exec erl \
    -noshell \
    -pa ebin deps/*/ebin \
    -boot start_sasl \
    -sname chatroom_dev \
    -s chatroom \
    -s reloader
