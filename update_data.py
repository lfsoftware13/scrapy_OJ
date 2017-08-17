from database.constants import problem_u_log, problem_u_pid, submit_u_log, submit_u_pid, problem_u_start_rediskey
import os
from util.ScriptsUtil import initLogging
import logging
from redis_database.redis_util import list_push
import time

problem_u_start = 'nohup /home/lf/anaconda3/bin/scrapy crawl problem_update >>'+problem_u_log+' 2>&1 & echo $! >> '+problem_u_pid
submit_u_start = 'nohup /home/lf/anaconda3/bin/scrapy crawl submit_update >>'+submit_u_log+' 2>&1 & echo $! >> '+submit_u_pid

def update():
    initLogging()
    os.chdir('/home/lf/DataCrawl/scrapy_OJ')
    if not os.path.exists('log/'):
        os.makedirs('log/')
    if not os.path.exists('crawl_state/'):
        os.makedirs('crawl_state/')
    if not os.path.exists('pid/'):
        os.makedirs('pid/')

    list_push(problem_u_start_rediskey, 'http://codeforces.com/problemset/page/1')

    res = os.system(problem_u_start)
    if res == 0:
        logging.info('[Start Problem Update Spider Success.]')
    else:
        logging.error('[Start Problem Update Spider Failed. Please check ' + problem_u_log+']')

    time.sleep(10)

    res = os.system(submit_u_start)
    if res == 0:
        logging.info('[Start Submit Update Spider Success.]')
    else:
        logging.error('[Start Submit Update Spider Failed. Please check ' + submit_u_log+']')

update()
