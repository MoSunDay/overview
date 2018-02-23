from flask import Flask, request
import pymysql as mysql

app = Flask(__name__)
db = mysql.connect(host='xxx.xxx.xxx.xxx', port=3306, user='xxx', passwd='xxx', db='xxx')
db_cur = db.cursor()

@app.route("/test/", methods=['GET'])
def test():
    return 'hello world'

@app.route("/overview/<project>", methods=['POST'])
def post_data(project):
    wait_write_to_mysql = request.get_json()
    print wait_write_to_mysql
    if project == 'cpu_status':
        db_cur.execute("insert cpu_status(cpu_load, time_now, host_name) values(%s, %s, %s)",
                       (wait_write_to_mysql['cpu_load'], wait_write_to_mysql['time_now'],
                        wait_write_to_mysql['host_name']))
        db.commit()
    elif project == 'tcp_status':
        db_cur.execute("insert tcp_status(listen, established, timewait, synrecv, finwait1, finwait2, lastack, time_now, host_name) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (wait_write_to_mysql['listen'], wait_write_to_mysql['established'], wait_write_to_mysql['timewait'],
                        wait_write_to_mysql['synrecv'], wait_write_to_mysql['finwait1'], wait_write_to_mysql['finwait2'],
                        wait_write_to_mysql['lastack'], wait_write_to_mysql['time_now'], wait_write_to_mysql['host_name']))
    elif project == 'mem_status':
        db_cur.execute("insert mem_status(used, time_now, host_name) values(%s, %s, %s)",
                       (wait_write_to_mysql['used'],  wait_write_to_mysql['time_now'], wait_write_to_mysql['host_name']))
        db.commit()
    elif project == 'io_status':
        db_cur.execute("insert io_status(io_wait, time_now, host_name) values(%s, %s, %s)",
                       (wait_write_to_mysql['io_wait'], wait_write_to_mysql['time_now'], wait_write_to_mysql['host_name']))
        db.commit()
    elif project == 'network_status':
        db_cur.execute("insert network_status(lan_rx, lan_tx, wlan_rx, wlan_tx, time_now, host_name) values(%s, %s, %s, %s, %s, %s)",
                       (wait_write_to_mysql['lan_rx'], wait_write_to_mysql['lan_tx'], wait_write_to_mysql['wlan_rx'],
                       wait_write_to_mysql['wlan_tx'], wait_write_to_mysql['time_now'], wait_write_to_mysql['host_name']))
        db.commit()
    else:
        return 'nothing'
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
