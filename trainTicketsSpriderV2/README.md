TODO:定时循环采集
目前的方案是利用linux的crontab来实现定时调度任务。
正在寻找更好的方法。


#部署

    pip install -r requirements.txt

启动redis

    redis-server

启动应用

    supervisord -c ./supervisor.conf


访问http://locahost:5000

利用crontab调度

	0 9 * * *  python ~/Reptile/trainTicketsSpriderV2/pullinRQ.py 9am
	0 11 * * * python ~/Reptile/trainTicketsSpriderV2/pullinRQ.py 11am
	0 15 * * * python ~/Reptile/trainTicketsSpriderV2/pullinRQ.py 3pm
	0 17 * * * python ~/Reptile/trainTicketsSpriderV2/pullinRQ.py 5pm
