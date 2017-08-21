from pause_spider import readPid
from database.constants import problem_u_pid, submit_u_pid
import os
import logging
from util.ScriptsUtil import initLogging

command_2 = "kill -2 "
command_9 = "kill -9 "

def pauseUpdate():
    initLogging()
    os.chdir('/home/lf/DataCrawl/scrapy_OJ')
    pro_pid = readPid(problem_u_pid)
    sub_pid = readPid(submit_u_pid)

    res = 0
    if pro_pid:
        res = os.system(command_2 + pro_pid)
    if not pro_pid:
        logging.info('[Problem Update Spider does not Run.]')
    elif res == 0:
        logging.info("[Pause Problem Update Spider Success.]")
    else:
        logging.error("[Pause Problem Update Spider Failed.]")

    res = 0
    if sub_pid:
        res = os.system(command_2 + sub_pid)
    if not pro_pid:
        logging.info('[Submit Update Spider does not Run.]')
    elif res == 0:
        logging.info("[Pause Submit Update Spider Success.]")
    else:
        logging.error("[Pause Submit Update Spider Failed.]")

pauseUpdate()
