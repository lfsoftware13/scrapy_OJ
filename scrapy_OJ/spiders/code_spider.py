from scrapy_OJ.items import CodeItem
from scrapy_redis.spiders import RedisCrawlSpider
from redis_database.redis_util import list_push
from database.constants import code_start_rediskey, code_error_rediskey
import logging


code_conn = None
count = 0
logger = logging.getLogger(__name__)

class CodeSpider(RedisCrawlSpider):
    name = 'code'
    allowed_domains = ['codeforces.com']
    redis_key = code_start_rediskey

    def parse(self, response):

        if response.status != 200 and response.status != 304:
            logging.error('[' + str(response.status) + '][0][' + response.url + ']')
            list_push(code_error_rediskey, response.url)
            return

        codes = response.selector.xpath('//pre[contains(@class, "program-source")]/text()').extract()

        logging.info('[' + str(response.status) + '][' + str(len(codes)) + '][' + response.url + ']')

        url = response.url
        id = (url.split('/')[-1])
        item = CodeItem()
        item['id'] = id
        item['code'] = codes[0]
        yield item
