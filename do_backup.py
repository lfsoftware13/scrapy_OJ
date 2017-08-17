from pause_spider import pauseSpider
from start_spider import start
from backup_data import backup
from util.ScriptsUtil import initLogging
import logging
import os
import time

def main():
    initLogging()
    logging.info('[Start backup]')
    os.chdir('/home/lf/DataCrawl/scrapy_OJ')
    pauseSpider()
    time.sleep(10)
    backup()
    start()
    logging.info('[End backup]')

main()
