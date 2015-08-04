

-module(chatroom_app).
-behaviour(application).
-export([start/2,stop/1]).

%% @spec start(_Type, _StartArgs) -> ServerRet
%% @doc application start callback for chatroom.
start(_Type, _StartArgs) ->
    chatroom_deps:ensure(),
    chatroom_sup:start_link().

%% @spec stop(_State) -> ServerRet
%% @doc application stop callback for chatroom.
stop(_State) ->
    ok.
