import scrapy
from scrapy import signals
from scrapy.http import HtmlResponse, Request, FormRequest
from util.CookieUtil import getCookieObject
from util.SpiderUtil import getPage
from scrapy_OJ.items import ProblemItem
from redis_database.redis_util import list_push, llendb, list_pop, list_push_left
from scrapy_redis.spiders import RedisCrawlSpider
from database.constants import CODEFORCE_DOMAIN
from scrapy.exceptions import CloseSpider
from database.constants import problem_u_start_rediskey, problem_u_error_rediskey, submit_u_start_rediskey
import logging


count_page = 0
count_item = 0

class ProblemSpider(RedisCrawlSpider):
    name = 'problem_update'
    allowed_domains = ['codeforces.com']
    redis_key = problem_u_start_rediskey

    def spider_idle(self):
        global count_page, count_item
        logging.info("[Update Problem Finish. %s Pages and %s ProblemItem were Updated.]", count_page, count_item)

    def parse(self, response):
        global count_page, count_item

        if response.status != 200 and response.status != 304:
            logging.error('[' + str(response.status) + '][0][' + response.url + ']')
            list_push(problem_u_error_rediskey, response.url)
            return

        count_page += 1
        problems = response.xpath("//table[@class='problems']/tr")

        logging.info('[' + str(response.status) + '][' + str(len(problems)-1) + '][' + response.url + ']')

        for pro in problems:
            tds = pro.xpath("td")
            if len(tds) == 0:
                continue
            count_item += 1
            item = ProblemItem()
            item['problem_name'] = [s.replace(u'\r\n', '').strip() for s in tds[0].xpath("a/text()").extract()]
            item['problem_url'] = [s.replace(u'\r\n', '').strip() for s in tds[0].xpath("a/@href").extract()]
            item['problem_des_name'] = [s.replace(u'\r\n', '').strip() for s in tds[1].xpath("div")[0].xpath("a/text()").extract()]
            item['tags'] = [s.replace(u'\r\n', '').strip() for s in tds[1].xpath("div")[1].xpath("a/text()").extract()]
            item['submit_urls'] = [s.replace(u'\r\n', '').strip() for s in tds[3].xpath("a/@href").extract()]
            for u in item['submit_urls']:
                list_push(submit_u_start_rediskey, CODEFORCE_DOMAIN + u)
            yield item

        (firstPage, lastPage, activePage, pageNext, firstPageUrl, lastPageUrl, activePageUrl, pageNextUrl) = getPage(response)

        if activePage != lastPage:
            yield Request(pageNextUrl, dont_filter=True)


