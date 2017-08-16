from scrapy import signals
import logging
from scrapy.exceptions import NotConfigured
from scrapy.http import Request

logger = logging.getLogger(__name__)

class CodeUrlAdd(object):
    def __init__(self, code_batch):
        self.code_batch = code_batch
        self.item_count = 0

    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise

        # NotConfigured otherwise
        # if not crawler.settings.getbool('MYEXT_ENABLED'):
        #     raise NotConfigured

        # get the number of items from settings
        code_batch = crawler.settings.getint('code_batch', 100)

        # instantiate the extension object
        ext = cls(code_batch)

        # connect the extension object to signals
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)

        # return the extension object
        return ext

    def item_scraped(self, item, spider):
        self.item_count += 1
        if self.item_count % self.code_batch == 0:
            logger.info("scraped %d items", self.item_count)
            f = open(r'C:\Users\Lf\Desktop\spider\code_record.txt', 'a')
            f.write("scraped "+str(self.item_count)+" items")
            f.close()

            yield Request('http://codeforces.com/problemset/status/71/problem/A/page/31?order=BY_ARRIVED_DESC', priority=9999, dont_filter=True)
