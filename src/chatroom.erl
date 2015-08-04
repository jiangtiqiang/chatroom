
-module(chatroom).
-export([start/0, stop/0]).

ensure_started(App) ->
    case application:start(App) of
        ok ->
            ok;
        {error, {already_started, App}} ->
            ok
    end.


%% @spec start() -> ok
%% @doc Start the chatroom server.
start() ->
    chatroom_deps:ensure(),
    ensure_started(crypto),
    application:start(chatroom).


%% @spec stop() -> ok
%% @doc Stop the chatroom server.
stop() ->
    application:stop(chatroom).
