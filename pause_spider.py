from database.constants import problem_pid, submit_pid, code_pid, presis_pid
from util.ScriptsUtil import initLogging
import logging
import os

command = 'kill -2 '

def readPid(file_path):
    pid = None
    if not os.path.exists(file_path):
        return None
    f = open(file_path, 'r')
    while 1:
        line = f.readline()
        if not line:
            break
        pid = line
    if not pid:
        logging.error(file_path+": pid not exist.")
    return pid

def readAllPid():
    pids = {}
    pids['problem'] = readPid(problem_pid)
    pids['submit'] = readPid(submit_pid)
    pids['code'] = readPid(code_pid)
    pids['presis'] = readPid(presis_pid)
    return pids

def pauseSpider():
    initLogging()
    pids = readAllPid()

    res = 0
    if pids['problem']:
        res = os.system(command+pids['problem'])
    if not pids['problem']:
        logging.info('[Problem Spider does not Run.]')
    elif res == 0:
        logging.info("[Pause Problem Spider Success.]")
    else:
        logging.error("[Pause Problem Spider Failed.]")

    res = 0
    if pids['submit']:
        res = os.system(command + pids['submit'])
    if not pids['submit']:
        logging.info('[Submit Spider does not Run.]')
    elif res == 0:
        logging.info("[Pause Submit Spider Success.]")
    else:
        logging.error("[Pause Submit Spider Failed.]")

    res = 0
    if pids['code']:
        res = os.system(command + pids['code'])
    if not pids['code']:
        logging.info('[Code Spider does not Run.]')
    elif res == 0:
        logging.info("[Pause Code Spider Success.]")
    else:
        logging.error("[Pause Code Spider Failed.]")

    res = 0
    if pids['presis']:
        res = os.system(command + pids['presis'])
    if not pids['presis']:
        logging.info('[Presis Item does not Run.]')
    elif res == 0:
        logging.info("[Pause Presis Item Success.]")
    else:
        logging.error("[Pause Presis Item Failed.]")

pauseSpider()
