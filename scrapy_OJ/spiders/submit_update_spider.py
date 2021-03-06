from scrapy.http import Request, FormRequest
from scrapy_OJ.items import SubmitItem
from scrapy_redis.spiders import RedisCrawlSpider
import logging
from redis_database.redis_util import list_push, list_pop
from util.CookieUtil import getCookieObject
from util.SpiderUtil import getPage
from database.constants import CODEFORCE_DOMAIN
from database.constants import submit_u_start_rediskey, submit_u_error_rediskey, submit_u_cookidwait_rediskey, code_start_rediskey
import datetime

in_request = 0
count_page = 0
count_item = 0

class SubmitSpider(RedisCrawlSpider):
    name = 'submit_update'
    allowed_domains = ['codeforces.com']
    redis_key = submit_u_start_rediskey

    def is_newest(self, submit_time_str):
        sub_time = datetime.datetime.strptime(submit_time_str, "%Y-%m-%d %H:%M:%S")
        one_day = datetime.timedelta(days=1)
        yes_time = (datetime.datetime.now()-one_day).replace(hour=0, minute=0, second=0, microsecond=0)
        return yes_time < sub_time

#    def spider_idle(self):
#        global count_page, count_item
#        logging.info("[Update Submit Finish. %s Pages and %s ProblemItem were Updated.]", count_page, count_item)

    def error(self, failure):
        logging.error('[FAILURE][FILTER][FILTER REQUEST FAILED.]')
        global in_request
        in_request = 0

    def after_filter(self, response):
        global in_request
        in_request = 0

        logging.info('[' + str(response.status) + '][FILTER][' + response.url + ']')
        url_bytes = list_pop(submit_u_cookidwait_rediskey)
        while url_bytes:
            url = str(url_bytes, encoding="utf-8")
            yield Request(url, dont_filter=True)
            url_bytes = list_pop(submit_u_cookidwait_rediskey)

    def parse(self, response):
        global count_page
        count_item = 0
        if response.status != 200 and response.status != 304:
            logging.error('[' + str(response.status) + '][0][' + response.url + ']')
            list_push(submit_u_error_rediskey, response.url)
            return

        trs = response.selector.xpath('//table[@class="status-frame-datatable"]/tr[@data-submission-id]')
        #logging.info('['+str(response.status)+']['+str(len(trs))+']['+response.url+']')

        opt = response.selector.xpath("//select[@name='verdictName']/option[@selected]/@value")
        global in_request

        if in_request == 1:
            list_push(submit_u_cookidwait_rediskey, response.url)
            logging.info('['+str(response.status)+']['+str(len(trs))+']['+response.url+'][WAIT]')
            return

        if opt.extract()[0] != 'anyVerdict':
            in_request = 1
            cookie_ob = getCookieObject(response)
            # print("cookid"+str(cookie_ob))
            csrf = response.selector.xpath('//span[@class="csrf-token"]/@data-csrf').extract()[0]
            yield FormRequest('http://codeforces.com/problemset/status/71/problem/A/page/1?order=BY_ARRIVED_DESC',
                              # meta={'dont_merge_cookies': True, 'cookiejar': response.meta['cookiejar']},
                              formdata={'csrf_token': csrf, 'action': 'setupSubmissionFilter', 'frameProblemIndex': 'A',
                                        'verdictName': 'anyVerdict',
                                        'programTypeForInvoker': 'anyProgramTypeForInvoker',
                                        'comparisonType': 'NOT_USED', 'judgedTestCount': '', '_tta': '795'},
                              callback=self.after_filter,
                              cookies=cookie_ob,
                              errback=self.error,
                              dont_filter=True
                              )
            list_push(submit_u_cookidwait_rediskey, response.url)
            return

        count_page += 1
        for tr in trs:
            tds = tr.xpath("td")
            item = SubmitItem()
            item['id'] = [s.replace(u'\r\n', '').strip() for s in tds[0].xpath('a/text()').extract()]
            item['submit_url'] = [s.replace(u'\r\n', '').strip() for s in tds[0].xpath('a/@href').extract()]
            item['submit_time'] = [s.replace(u'\r\n', '').strip() for s in tds[1].xpath('text()').extract()]
            item['user_id'] = [s.replace(u'\r\n', '').strip() for s in tds[2].xpath('@data-participantid').extract()]
            item['user_name'] = [s.replace(u'\r\n', '').strip() for s in tds[2].xpath('a/text()').extract()]
            item['problem_id'] = [s.replace(u'\r\n', '').strip() for s in tds[3].xpath('@data-problemid').extract()]
            item['problem_url'] = [s.replace(u'\r\n', '').strip() for s in tds[3].xpath('a/@href').extract()]
            item['problem_full_name'] = [s.replace(u'\r\n', '').strip() for s in tds[3].xpath('a/text()').extract()]
            item['language'] = [s.replace(u'\r\n', '').strip() for s in tds[4].xpath('text()').extract()]
            item['status'] = [s.replace(u'\r\n', '').strip() for s in tds[5].xpath('span/@submissionverdict').extract()]
            item['error_test_id'] = [s.replace(u'\r\n', '').strip() for s in tds[5].xpath('span/span/span/text()').extract()]
            item['time'] = [s.replace(u'\xa0', '').replace(u'\r\n', '').strip() for s in tds[6].xpath('text()').extract()]
            item['memory'] = [s.replace(u'\xa0', '').replace(u'\r\n', '').strip() for s in tds[7].xpath('text()').extract()]

            if not self.is_newest(item['submit_time'][0]):
                logging.info('[' + str(response.status) + '][' + str(count_item) + '][' + response.url + ']')
                return

            count_item += 1
            yield item
            for u in item['submit_url']:
                list_push(code_start_rediskey, CODEFORCE_DOMAIN+u)

        logging.info('[' + str(response.status) + '][' + str(count_item) + '][' + response.url + ']')

        (firstPage, lastPage, activePage, pageNext, firstPageUrl, lastPageUrl, activePageUrl, pageNextUrl) = getPage(response)

        if activePage != lastPage:
            yield Request(pageNextUrl, dont_filter= True)






