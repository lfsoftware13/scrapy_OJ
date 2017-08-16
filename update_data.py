from database.constants import problem_u_log, problem_u_pid, submit_u_log, submit_u_pid
import os
from util.ScriptsUtil import initLogging
import logging

problem_u_start = 'nohup scrapy crawl problem_update >'+problem_u_log+' 2>&1 & echo $! >> '+problem_u_pid
submit_u_start = 'nohup scrapy crawl submit_update >'+submit_u_log+' 2>&1 & echo $! >> '+submit_u_pid

def update():
    initLogging()
    if not os.path.exists('log/'):
        os.makedirs('log/')
    if not os.path.exists('crawl_state/'):
        os.makedirs('crawl_state/')
    if not os.path.exists('pid/'):
        os.makedirs('pid/')

    res = os.system(problem_u_start)
    if res == 0:
        logging.info('[Start Problem Update Spider Success.]')
    else:
        logging.error('[Start Problem Update Spider Failed. Please check ' + problem_u_log+']')

    res = os.system(submit_u_start)
    if res == 0:
        logging.info('[Start Problem Update Spider Success.]')
    else:
        logging.error('[Start Problem Update Spider Failed. Please check ' + submit_u_log+']')

update()