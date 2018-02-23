{{toc/}}

---

# overview

## 指标

展示的内容有：

- 所有监控的主机:`all_hosts_num`;

- 所有监控的组:`groups_num`;

- 当前组的主机数量:`hosts_num`;

- 组内主机的`cpu load`以及`最值`和`平均值`;

- 组内主机的`mem used`以及`最值`和`平均值`;

- 组内主机的`网卡流量`以及`最值`和`平均值`;

- 组内主机的`iowait`以及`最值`和`平均值`;

- 组内主机的`tcp`状态以及数值`之和`;

## 思路

构建监控的思路如下：

- 将`主机名`和`组名`以`.yml`格式保存下来，通过脚本解析，自动在数据库中创建对应关系，当有主机名更改和组名更改时，只需重新跑一次脚本即可;
- 在`server`端启动`汇聚信息`并以主机为单位`写入`数据库的服务;
- 在`client`端启动`agent`来定时获取数据;

总的来说，`client`给`server`提供以`主机名`为表示的数据，`主机名`和`组名`的关系通过`数据库的数据`来构建，而`数据`是可以通过`.yml`文件来自动生成的。