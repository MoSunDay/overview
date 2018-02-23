import socket
import subprocess
import time
import json
from datetime import datetime

import requests
from requests.exceptions import ConnectionError

overview_host="xxx.xxx.xxx.xxx"

def get_net_info():
    temp = subprocess.Popen("cat /proc/net/dev | egrep 'eth0|eth1' | awk '{print $2, $10}'", shell=True, stdout=subprocess.PIPE)
    temp_list = temp.stdout.readlines()
    net_data_one = ''.join(temp_list).split()
    time.sleep(2)
    temp = subprocess.Popen("cat /proc/net/dev | egrep 'eth0|eth1' | awk '{print $2, $10}'", shell=True, stdout=subprocess.PIPE)
    temp_list = temp.stdout.readlines()
    net_data_two = ''.join(temp_list).split()
    net_data = []
    for n in xrange(4):
        net_data.append((int(net_data_two[n]) - int(net_data_one[n])) / 2)
    return net_data

def get_cpu_info():
    temp = subprocess.Popen("uptime | grep -Po 'load average:.*' | awk -F '[: ,]+' '{print $3}'", shell=True, stdout=subprocess.PIPE)
    cpu_info_data = temp.stdout.readline().strip()
    temp = subprocess.Popen("cat /proc/cpuinfo | grep \"cpu cores\"| uniq | awk '{print $4}'", shell=True, stdout=subprocess.PIPE)
    cpu_core = int(temp.stdout.readline().strip())

    return float(cpu_info_data) / cpu_core

def get_disk_info():
    temp = subprocess.Popen("iostat | grep -A 1 '%iowait'|awk 'NR==2{print $4}'", shell=True, stdout=subprocess.PIPE)
    return float(temp.stdout.readline().strip())

def get_tcp_info():
    temp = subprocess.Popen("ss -a | grep '\\bLISTEN\\b'|wc -l", shell=True, stdout=subprocess.PIPE)
    listen_num = temp.stdout.readline().strip()
    temp = subprocess.Popen("ss -a | grep '\\bESTAB\\b'|wc -l", shell=True, stdout=subprocess.PIPE)
    established_num = temp.stdout.readline().strip()
    temp = subprocess.Popen("ss -a | grep '\\bTIME-WAIT\\b'|wc -l", shell=True, stdout=subprocess.PIPE)
    timewait_num = temp.stdout.readline().strip()
    temp = subprocess.Popen("ss -a | grep '\\bSYN-RECV\\b'|wc -l", shell=True, stdout=subprocess.PIPE)
    synrecv_num = temp.stdout.readline().strip()
    temp = subprocess.Popen("ss -a | grep '\\bFIN-WAIT-1\\b'|wc -l", shell=True, stdout=subprocess.PIPE)
    finwait1_num = temp.stdout.readline().strip()
    temp = subprocess.Popen("ss -a | grep '\\bFIN-WAIT-2\\b'|wc -l", shell=True, stdout=subprocess.PIPE)
    finwait2_num = temp.stdout.readline().strip()
    temp = subprocess.Popen("ss -a | grep '\\LAST-ACK\\b'|wc -l", shell=True, stdout=subprocess.PIPE)
    lastack_num = temp.stdout.readline().strip()
    return listen_num, established_num, timewait_num, synrecv_num, finwait1_num, finwait2_num, lastack_num

def get_mem_info():
    # temp = subprocess.Popen("free -m | awk 'NR==2{print $3}'", shell=True, stdout=subprocess.PIPE)
    # used = temp.stdout.readline().strip()
    # temp = subprocess.Popen("free -m | awk 'NR==2{print $4}'", shell=True, stdout=subprocess.PIPE)
    # free = temp.stdout.readline().strip()
    # temp = subprocess.Popen("free -m | awk 'NR==2{print $6}'", shell=True, stdout=subprocess.PIPE)
    # buffer = temp.stdout.readline().strip()
    # temp = subprocess.Popen("free -m | awk 'NR==2{print $7}'", shell=True, stdout=subprocess.PIPE)
    # cached = temp.stdout.readline().strip()
    # temp = subprocess.Popen("free -m | awk 'NR==2{print $2}'", shell=True, stdout=subprocess.PIPE)
    # total = temp.stdout.readline().strip()
    temp = subprocess.Popen("free -m | awk -F '[  ]+' 'NR==3{print $3}'", shell=True, stdout=subprocess.PIPE)
    used = temp.stdout.readline().strip()
    temp = subprocess.Popen("free -m | awk -F '[  ]+' 'NR==2{print $2}'", shell=True, stdout=subprocess.PIPE)
    total = temp.stdout.readline().strip()
    return float(used) / int(total)

if __name__ == '__main__':
    headers = {'Content-type': 'application/json'}
    while True:
        cpu_data = get_cpu_info()
        net_data = get_net_info()
        disk_data = get_disk_info()
        tcp_data = get_tcp_info()
        mem_data = get_mem_info()
        try:
            overview_agent = requests.post("http://{0}:5000/overview/cpu_status".format(overview_host), headers=headers, data=json.dumps({
                "cpu_load": float('%.2f' % cpu_data),
                "host_name": socket.gethostname(),
                "time_now": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }))
            overview_agent = requests.post("http://{0}:5000/overview/network_status".format(overview_host), headers=headers, data=json.dumps({
                "lan_rx": int(net_data[2]),
                "lan_tx": int(net_data[3]),
                "wlan_rx": int(net_data[0]),
                "wlan_tx": int(net_data[1]),
                "host_name": socket.gethostname(),
                "time_now": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }))
            overview_agent = requests.post("http://{0}:5000/overview/io_status".format(overview_host), headers=headers, data=json.dumps({
                "io_wait": float('%.2f' % disk_data),
                "host_name": socket.gethostname(),
                "time_now": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }))
            overview_agent = requests.post("http://{0}:5000/overview/tcp_status".format(overview_host), headers=headers, data=json.dumps({
                'listen': int(tcp_data[0]),
                'established': int(tcp_data[1]),
                'timewait': int(tcp_data[2]),
                'synrecv': int(tcp_data[3]),
                'finwait1': int(tcp_data[4]),
                'finwait2': int(tcp_data[5]),
                'lastack': int(tcp_data[6]),
                "host_name": socket.gethostname(),
                "time_now": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }))
            overview_agent = requests.post("http://{0}:5000/overview/mem_status".format(overview_host), headers=headers, data=json.dumps({
                "used": float('%.2f' % mem_data),
                "host_name": socket.gethostname(),
                "time_now": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }))
        except ConnectionError:
            pass
        time.sleep(57)