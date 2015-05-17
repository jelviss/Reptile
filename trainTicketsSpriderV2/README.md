TODO:定时循环采集
目前的方案是利用linux的crontab来实现定时调度任务。
正在寻找更好的方法。


#部署

        python setup.py

- 启动redis

        redis-server

- 配置email.conf

- 启动应用

        supervisord -c ./supervisor.conf


- 利用crontab调度(假设项目在用户家目录下)

        0 9 * * *  ~/Reptile/trainTicketsSpriderV2/flask/bin/python ~/Reptile/trainTicketsSpriderV2/pullinRQ.py 9am
        0 11 * * * ~/Reptile/trainTicketsSpriderV2/flask/bin/ ~/Reptile/trainTicketsSpriderV2/pullinRQ.py 11am
        0 15 * * * ~/Reptile/trainTicketsSpriderV2/flask/bin/ ~/Reptile/trainTicketsSpriderV2/pullinRQ.py 3pm
        0 17 * * * ~/Reptile/trainTicketsSpriderV2/flask/bin/ ~/Reptile/trainTicketsSpriderV2/pullinRQ.py 5pm

- 控制服务

        supervisorctl -c ./supervisor.conf start ttsprider
        supervisorctl -c ./supervisor.conf stop ttsprider

访问http://locahost:9999
