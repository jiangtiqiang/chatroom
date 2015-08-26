#!/usr/bin/env python


import urllib2
import json
import os
import time


class Template():
    def __init__(self):
        self.title = "listen "
        self.bind = ""
        self.mode = "tcp"
        self.option = "tcplog"
        self.balance = "leastconn"


class Fresh():
    def __init__(self):
        self.current_json = ""
        self.new_json = ""
        self.marathon_url = "http://10.16.83.52:8080/v2/tasks"
        self.port_url = "http://10.16.83.52:4001/v2/keys/"
        self.config_file = "haproxy.cfg"
        self.history_json_url = "history.json"
        self.id_dic = {}
        self.hot_update_cmd = "haproxy -f /etc/haproxy/haproxy.cfg -p haproxy.pid -sf"
        self.head = "global  \n" \
                    "  daemon \n" \
                    "  log 127.0.0.1 local0 \n" \
                    "  log 127.0.0.1 local1 notice \n" \
                    "  maxconn 100000 \n \n" \
                    "  defaults\n" \
                    "  log            global\n" \
                    "  retries             3\n" \
                    "  maxconn          100000\n" \
                    "  timeout connect  5000\n" \
                    "  timeout client  50000\n" \
                    "  timeout server  50000\n\n" \
                    "  listen stats\n" \
                    "  bind 127.0.0.1:9090\n" \
                    "  balance\n" \
                    "  mode http\n" \
                    "  stats enable\n" \
                    "  stats auth admin:admin\n\n"

    def get_port(self):
        try:
            response = urllib2.urlopen(self.port_url, None, 2000)
            resp_str = json.loads(response.read())
            node = resp_str["node"]
            nodes = node["nodes"]
            for item in nodes:
                try:
                    int(item["value"])
                    name = item["key"][1:]
                    self.id_dic[name] = item["value"]
                except Exception:
                    pass
        except Exception:
            pass

    def init_data(self):
        if os.path.exists(self.history_json_url):
            f = open(self.history_json_url)
            try:
                self.current_json = f.read()
            finally:
                f.close()

    def get_json(self):
        try:
            response = urllib2.urlopen(self.marathon_url, None, 2000)
            json_str = response.read()
            self.new_json = json.loads(json_str)["tasks"]
        except Exception:
            pass

    def compare_equal(self):
        for item in self.new_json:
            try:
                item["healthCheckResults"] = ""
                item["version"] = ""
                item["startedAt"] = ""
            except Exception:
                pass
        result = self.current_json == self.new_json
        self.current_json = self.new_json
        if not result:
            f = open(self.history_json_url, "w")
            try:
                f.writelines(str(self.current_json))
            finally:
                f.close()
        return result

    def create_config(self):
        f = open(self.config_file, "w")
        try:
            f.writelines(self.head)
            lst = self.new_json
            id_list = []
            for item in lst:
                id_list.append(item["id"][0:10])
            id_list = list(set(id_list))  # unique id
            for app_id in id_list:
                map_relation = "\n\nlisten  " + app_id + "\n" \
                                                         "  bind  0.0.0.0:" + self.id_dic[app_id] + "\n" \
                                                                                                    "  mode tcp\n" \
                                                                                                    "  option tcplog\n" \
                                                                                                    "  balance leastconn\n"
                i = 0
                for task in lst:
                    if task["id"][0:10] == app_id:
                        map_relation += "  server  " + app_id + str(i) + "  " + task["host"] + ":" + str(
                            task["ports"][0]) + "\n"
                        i += 1
                f.writelines(map_relation)
        except Exception:
            pass
        finally:
            f.close()

    def hot_fresh(self):
        os.system(self.hot_update_cmd)

    def job_console(self):
        self.init_data()
        self.get_port()
        self.get_json()
        while True:
            if not self.compare_equal():
                self.create_config()
                self.hot_fresh()
                #print "--------------------------------------------------find"
            self.get_port()
            self.get_json()
            time.sleep(1)
           # print "working"


worker = Fresh()
worker.job_console()
