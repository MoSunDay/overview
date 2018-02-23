#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
from get_groups_hosts import GroupsHosts

class MysqlStorage():
    def __init__(self):
        self.mysql_client = pymysql.connect(host='xxx.xxx.xxx.xxx', port=3306, user='xxx', passwd='xxxx', db='xxxx')
        self.mysql_cur = self.mysql_client.cursor()
        self._groups_hosts_data = groups_hosts_data

    def create_measure_groups(self):
        self.mysql_cur.execute('DROP TABLE IF EXISTS `groups_and_hosts`;')
        self.mysql_client.commit()
        self.mysql_cur.execute('''
            CREATE TABLE IF NOT EXISTS`groups_and_hosts`(
                `id` int(32) AUTO_INCREMENT,
                `group_name` varchar(32) NOT NULL,
                `host_name` varchar(32) NOT NULL,
                `time_now` TIMESTAMP NOT NULL,
                 PRIMARY KEY ( `id` )
            )ENGINE=InnoDB DEFAULT CHARSET=utf8;
        ''')
        self.mysql_client.commit()
        for group_name in self._groups_hosts_data.keys():
            for host_name in self._groups_hosts_data[group_name]:
                print group_name, host_name
                self.mysql_cur.execute("insert groups_and_hosts(group_name, host_name) VALUE (%s, %s)",
                                       (group_name, host_name))
                self.mysql_client.commit()
    def exit_close(self):
        self.mysql_cur.close()

if __name__ == '__main__':
    groups_hosts_obj = GroupsHosts()
    groups_hosts_data = groups_hosts_obj.overview_client_remove_hosts()
    mysql_obj = MysqlStorage()
    mysql_obj.create_measure_groups()
    mysql_obj.exit_close()
