from scrapy_OJ.items import CodeTestcaseItem
from scrapy_redis.spiders import RedisCrawlSpider
from redis_database.redis_util import list_push
from database.constants import code_testcase_start_rediskey, code_testcase_error_rediskey
import logging


code_conn = None
count = 0
logger = logging.getLogger(__name__)

class CodeTestcaseSpider(RedisCrawlSpider):
    name = 'code_testcase'
    allowed_domains = ['codeforces.com']
    redis_key = code_testcase_start_rediskey

    def parse(self, response):

        if response.status != 200 and response.status != 304:
            logging.error('[' + str(response.status) + '][0][' + response.url + ']')
            list_push(code_testcase_error_rediskey, response.url)
            return

        # codes = response.selector.xpath('//pre[contains(@class, "program-source")]/text()').extract()
        infolines = response.selector.xpath('//div[contains(@class, "infoline")]')
        infolines = infolines.xpath("string(.)").extract()
        verdicts = response.selector.xpath('//div[contains(@class, "infoline")]/div/text()').extract()
        inputs = response.selector.xpath('//div[contains(@class, "input-view")]/div[contains(@class, "text")]/pre/text()').extract()
        outputs = response.selector.xpath('//div[contains(@class, "output-view")]/div[contains(@class, "text")]/pre/text()').extract()
        answers = response.selector.xpath('//div[contains(@class, "answer-view")]/div[contains(@class, "text")]/pre/text()').extract()
        checkers = response.selector.xpath('//div[contains(@class, "checker-comment-view")]/div[contains(@class, "text")]/pre/text()').extract()

        infos = []
        for i in range(len(inputs)):
            infos += [infolines[i * 2]]

        logging.info('[' + str(response.status) + '][' + str(len(inputs)) + '][' + response.url + ']')

        print('infolines: ', infos)
        print('verdicts: ', verdicts)
        print('inputs: ', inputs)
        print('outputs: ', outputs)
        print('answers: ', answers)
        print('checkers: ', checkers)

        url = response.url
        id = (url.split('/')[-1])
        it_list = []
        for inf, ver, inp, out, ans, check in zip(infos, verdicts, inputs, outputs, answers, checkers):
            it = {'info': inf, 'verdict': ver, 'input': inp, 'output': out, 'answer': ans, 'checker_comment': check}
            it_list += [it]
        item = CodeTestcaseItem()
        item['id'] = id
        item['testcase'] = it_list
        yield item
