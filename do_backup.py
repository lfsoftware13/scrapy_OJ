from pause_spider import pauseSpider
from start_spider import start
from backup_data import backup
from util.ScriptsUtil import initLogging
import logging

def main():
    initLogging()
    logging.info('[Start backup]')
    pauseSpider()
    backup()
    start()
    logging.info('[End backup]')

main()
