TODO:定时循环采集
目前的方案是利用linux的crontab来实现定时调度任务。
正在寻找更好的方法。


#部署
项目默认放在`/var/www`下,如果放在其他目录,根据情况修改`supervisor.conf`和`crontab`配置即可

- 执行setup.py

        python setup.py

- 启动redis

        redis-server

- 配置tttsprider/ttsprider.conf

- 启动应用

        /var/www/Reptile/trainTicketsSpriderV2/flask/bin/supervisord -c ./supervisor.conf


- 利用crontab调度

        0 9 * * *  /var/www/Reptile/trainTicketsSpriderV2/flask/bin/python /var/www/Reptile/trainTicketsSpriderV2/ttsprider/pullinRQ.py 9am
        0 11 * * * /var/www/Reptile/trainTicketsSpriderV2/flask/bin/python /var/www/Reptile/trainTicketsSpriderV2/ttsprider/pullinRQ.py 11am
        0 15 * * * /var/www/Reptile/trainTicketsSpriderV2/flask/bin/python /var/www/Reptile/trainTicketsSpriderV2/ttsprider/pullinRQ.py 3pm
        0 17 * * * /var/www/Reptile/trainTicketsSpriderV2/flask/bin/python /var/www/Reptile/trainTicketsSpriderV2/ttsprider/pullinRQ.py 5pm

- 控制服务

        /var/www/Reptile/trainTicketsSpriderV2/flask/bin/supervisorctl -c ./supervisor.conf start ttsprider
        /var/www/Reptile/trainTicketsSpriderV2/flask/bin/supervisorctl -c ./supervisor.conf stop ttsprider

访问http://locahost:9999

---

#问题

第一次运行会报错`pkg_resources.DistributionNotFound: meld3>=0.6.5`

请再次运行setup.py
