#!/usr/bin/env python
# -*- coding: utf-8 -*-

from influxdb import InfluxDBClient
from get_groups_hosts import GroupsHosts

class influx(InfluxDBClient):
    def __init__(self, groups_hosts_data):
        super(influx, self).__init__(host='xxx.xxx.xxx.xxx', database="groups_map_hosts")
        self.drop_database("groups_map_hosts")
        self.create_database("groups_map_hosts")
        self.drop_database("groups_hosts_options")
        self.create_database("groups_hosts_options")
        self._groups_hosts_data = groups_hosts_data

    def create_measure_groups(self):
        for group_name in self._groups_hosts_data.keys():
            for host_name in self._groups_hosts_data[group_name]:
                wait_write_data = [
                    {
                        "measurement": group_name,
                        "tags": {
                            "host_tag": host_name,
                            "group_tag": group_name
                        },
                        "fields": {
                            "hostname": host_name,
                        }
                    }
                ]
                self.write_points(wait_write_data)
            self.switch_database("groups_hosts_options")
            for table in ["average", "total"]:
                wait_write_data = [
                    {
                        "measurement": group_name,
                        "tags": {
                            "hostname": table,
                            "groupname": group_name
                        },
                        "fields": {
                            "options": table
                        }
                    }
                ]
                self.write_points(wait_write_data)
            self.switch_database("groups_map_hosts")

if __name__ == '__main__':
    groups_hosts_obj = GroupsHosts()
    groups_hosts_data = groups_hosts_obj.overview_client_remove_hosts()
    influx_obj = influx(groups_hosts_data)
    influx_obj.create_measure_groups()