import os
from database.constants import DATABASE_PATH
import time
import shutil
from util.ScriptsUtil import initLogging
import logging

def backup():
    initLogging()
    backup_path = os.path.join("backup", time.strftime("%Y_%m_%d_%H_%M_%S"))

    if not os.path.exists(backup_path):
        os.makedirs(backup_path)

    data_path = os.path.join(backup_path, "scrapyOJ.db")
    crawl_path = os.path.join(backup_path, "crawl_state")
    log_path = os.path.join(backup_path, "log")
    shutil.copyfile(DATABASE_PATH, data_path)
    shutil.copytree("crawl_state/", crawl_path)
    shutil.copytree("log/", log_path)
    shutil.rmtree("log/")
    os.makedirs('log/')
    logging.info('[BACKUP]['+backup_path+']')

backup()