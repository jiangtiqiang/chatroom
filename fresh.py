import urllib2
import json
import os
import Queue


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
        self.marathon_url = "http://address/v2/tasks"
        self.port_url = "http://address:4001/v2/keys/"
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
                except Exception as e:
                    print e
        except Exception as e:
            print e

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
            self.new_json = json_str
        except Exception as e:
            print e

    def compare_equal(self):
        return self.current_json != self.new_json

    def create_config(self):
        f = open(self.config_file, "w")
        try:
            f.writelines(self.head)
            lst = json.loads(self.new_json)["tasks"]
            id_list = []
            for item in lst:
                id_list.append(item["id"][0, 10])
            list(set(id_list))  # unique id
            for app_id in id_list:
                map_relation = "\n\nlisten  " + app_id + "\n" \
                                                     "  bind  0.0.0.0:" + self.id_dic[app_id] + "\n" \
                                                                                                "  mode tcp\n" \
                                                                                                "  option tcplog\n" \
                                                                                                "  balance leastconn\n"
                i = 0
                for task in lst:
                    map_relation = map_relation + "  server  " + app_id + i + "  "+task["host"] + ":" + task["ports"][0]
                    i += 1
                f.writelines(map_relation)
        finally:
            f.close()

    def hot_fresh(self):
        os.system(self.hot_update_cmd)

    def job_console(self):
        self.init_data()
        self.get_port()
        self.get_json()
        self.compare_equal()
        #self.create_config()
        self.hot_fresh()
        # while True:
        # self.get_json()
        # time.sleep(1)


worker = Fresh()
worker.job_console()
