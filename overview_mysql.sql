
USE overview;
DROP TABLE tcp_status;
DROP TABLE cpu_status;
DROP TABLE network_status;
DROP TABLE io_status;
DROP TABLE mem_status;

CREATE TABLE IF NOT EXISTS `tcp_status` (
    `id` int(32) AUTO_INCREMENT,
    `listen` int(32) NOT NULL,
    `established` int(32) NOT NULL,
    `timewait` int(32) NOT NULL,
    `synrecv` int(32) NOT NULL,
    `finwait1` int(32) NOT NULL,
    `finwait2` int(32) NOT NULL,
    `lastack` int(32) NOT NULL,
    `time_now` TIMESTAMP NOT NULL,
    `host_name` VARCHAR(32) NOT NULL,
    PRIMARY KEY (`id`),
    INDEX(`time_now`, `host_name`)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `cpu_status`(
    `id` int(32) AUTO_INCREMENT,
    `cpu_load` FLOAT NOT NULL,
    `time_now` TIMESTAMP NOT NULL,
    `host_name` VARCHAR(32) NOT NULL,
    PRIMARY KEY (`id`),
    INDEX(`time_now`, `host_name`)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `network_status`(
    `id` int(32) AUTO_INCREMENT,
    `lan_rx` BIGINT NOT NULL,
    `lan_tx` BIGINT NOT NULL,
    `wlan_rx` BIGINT NOT NULL,
    `wlan_tx` BIGINT NOT NULL,
    `time_now` TIMESTAMP NOT NULL,
    `host_name` VARCHAR(32) NOT NULL,
    PRIMARY KEY (`id`),
    INDEX(`time_now`, `host_name`)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `io_status`(
    `id` int(32) AUTO_INCREMENT,
    `io_wait` FLOAT NOT NULL,
    `time_now` TIMESTAMP NOT NULL,
    `host_name` VARCHAR(32) NOT NULL,
    PRIMARY KEY (`id`),
    INDEX(`time_now`, `host_name`)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `mem_status`(
    `id` int(32) AUTO_INCREMENT,
    `used` FLOAT NOT NULL,
    `time_now` TIMESTAMP NOT NULL,
    `host_name` VARCHAR(32) NOT NULL,
    PRIMARY KEY (`id`),
    INDEX(`time_now`, `host_name`)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


SELECT
  FLOOR((UNIX_TIMESTAMP(time_now))/(60)) as time_tmp,
  UNIX_TIMESTAMP(time_now) as time_sec,
  max(cpu_load) as value,
  "cpu-load: max" as metric,
  host_name
FROM cpu_status
where host_name in (SELECT host_name from groups_and_hosts WHERE group_name='codis-proxy')
group by(time_tmp);

SELECT
    FLOOR((UNIX_TIMESTAMP(cpu_status.time_now))/(60)) as time_tmp,
    UNIX_TIMESTAMP(cpu_status.time_now) as time_sec,
    cpu_status.time_now,
    max(cpu_load) as value,
    t_gh.group_name
FROM cpu_status JOIN groups_and_hosts as t_gh ON t_gh.host_name=cpu_status.host_name
WHERE cpu_status.time_now >= FROM_UNIXTIME(1512036644)
      AND cpu_status.time_now <= FROM_UNIXTIME(1512040244)
GROUP BY t_gh.group_name, time_tmp;




