import os
from database.constants import problem_job, submit_job, code_job, problem_log, submit_log, code_log, presis_log, problem_pid, submit_pid, code_pid, presis_pid
from util.ScriptsUtil import initLogging
import logging

problem_start = 'nohup /home/lf/anaconda3/bin/scrapy crawl problem -s JOBDIR='+problem_job+'>>'+problem_log+' 2>&1 & echo $! >> '+problem_pid
submit_start = 'nohup /home/lf/anaconda3/bin/scrapy crawl submit -s JOBDIR='+submit_job+'>>'+submit_log+' 2>&1 & echo $! >> '+submit_pid
code_start = 'nohup /home/lf/anaconda3/bin/scrapy crawl code -s DOWNLOAD_DELAY=0.5 -s JOBDIR='+code_job+' >>'+code_log+' 2>&1 & echo $! >> '+code_pid

item_presis_start = 'nohup /home/lf/anaconda3/bin/python items_presis.py >>'+presis_log+' 2>&1 & echo $! >> '+presis_pid

def start():
    initLogging()
    if not os.path.exists('log/'):
        os.makedirs('log/')
    if not os.path.exists('crawl_state/'):
        os.makedirs('crawl_state/')
    if not os.path.exists('pid/'):
        os.makedirs('pid/')

    res = os.system(problem_start)
    if res == 0:
        logging.info('[Problem Spider start success]')
    else:
        logging.error('[Problem Spider start failed. Please check '+problem_log+']')

    res = os.system(submit_start)
    if res == 0:
        logging.info('[Submit Spider start success]')
    else:
        logging.error('[ERROR][Submit Spider start failed. Please check '+submit_log+']')

    res = os.system(code_start)
    if res == 0:
        logging.info('[Code Spider start success]')
    else:
        logging.error('[Code Spider start failed. Please check '+code_log+']')

    # res = os.system(item_presis_start)
    # if res == 0:
    #     logging.info('[Item Presistence start success]')
    # else:
    #     logging.error('[Item Presistence start failed. Please check '+presis_log+']')

