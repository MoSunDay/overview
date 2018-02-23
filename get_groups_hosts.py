#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict
import yaml
import copy

class GroupsHosts(object):
    def __init__(self):
        with open("group_and_host.yaml") as file:
            self._groups_hosts_data = yaml.load(file)
        self.groups_hosts = defaultdict(dict)

    def get_all_hosts(self, group):
        return self._groups_hosts_data[group]

    def test(self, group):
        return self._groups_hosts_data[group]

    def get_group_hosts_list(self):
        for group in self._groups_hosts_data.keys():
            yield group, self._groups_hosts_data[group]

    def is_groups(self, groups_or_hosts):
        return True if groups_or_hosts in self._groups_hosts_data.keys() else False

    def get_all_groups_hosts(self):
        temp_data = self.get_group_hosts_list()
        while True:
            try:
                group, groups_or_hosts = next(temp_data)
            except StopIteration:
                break
            else:
                hosts_data_temp = []
                def get_hosts_in_group(groups_or_hosts):
                    for group_or_host in groups_or_hosts:
                        if self.is_groups(group_or_host):
                                get_hosts_in_group(groups_or_hosts=self.get_all_hosts(group_or_host))
                        else:
                            hosts_data_temp.append(group_or_host)
                get_hosts_in_group(groups_or_hosts)
                self.groups_hosts[group] = set(hosts_data_temp)

    def overview_client_remove_hosts(self, group_list=None, host_list=None, group=None):
        self.get_all_groups_hosts()
        order_groups_hosts = copy.deepcopy(self.groups_hosts)
        if group_list is None and host_list is None and group is None:
            pass
        elif host_list is None and group_list is not None:
            for group in group_list:
                order_groups_hosts[group] = list(set(self.groups_hosts[group]) - set(order_groups_hosts[group]))

        elif host_list is not None and group is not None:
                order_groups_hosts[group] = list(set(order_groups_hosts[group]) - set(host_list))
        else:
            print("## func: overview_client_remove_hosts args error")
        return order_groups_hosts

if __name__ == '__main__':
    groups_hosts_obj = GroupsHosts()
    groups_hosts_data = groups_hosts_obj.overview_client_remove_hosts()
    for group in groups_hosts_data.keys():
        with open("" + group, "w") as file:
            for host in groups_hosts_data[group]:
                file.write(host + '\n')