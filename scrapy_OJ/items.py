# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SubmitItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    submit_url = scrapy.Field()
    submit_time = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    problem_id = scrapy.Field()
    problem_url = scrapy.Field()
    problem_full_name = scrapy.Field()
    language = scrapy.Field()
    status = scrapy.Field()
    error_test_id = scrapy.Field()
    time = scrapy.Field()
    memory = scrapy.Field()


class CodeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    code = scrapy.Field()


class CodeTestcaseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    testcase = scrapy.Field()


class ProblemItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    problem_name = scrapy.Field()
    problem_url = scrapy.Field()
    problem_des_name = scrapy.Field()
    tags = scrapy.Field()
    submit_urls = scrapy.Field()


