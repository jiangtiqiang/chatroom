import urllib2
import json
import os


class Template():
    def __init__(self):
        self.bind = ""
        self.appId = ""
        self.host = ""
        self.port = ""


class Fresh():
    def __init__(self):
        self.current_json = ""
        self.new_json = ""
        self.marathon_url = "http://localhost:8080/full/api/book/get"
        self.port_url = ""
        self.config_file = "haproxy.cfg"
        self.history_json_url = "history.json"

    def get_port(self, appId):
        try:
            response = urllib2.urlopen(self.marathon_url, None, 2000)
            bind_port = response.read()
            return bind_port
        except Exception as e:
            print e

    def init_data(self):
        f = open(self.history_json_url)
        try:
            if os.path.exists(self.history_json_url):
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
            lst = json.loads(self.current_json)
            id_list = []
            for item in lst:
                id_list.append(item["id"][0, 10])
            list(set(id_list))  # unique id

        finally:
            f.close()


def job_console(self):
    self.init_data()
    self.get_json()
    self.create_config()
    self.compare_equal()
    # while True:
    # self.get_json()
    # time.sleep(1)


worker = Fresh()
worker.job_console()
