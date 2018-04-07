# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from database.database_util import insertSubmit, insertCode
from scrapy_OJ.spiders.code_spider import code_conn
from scrapy_OJ.items import SubmitItem, CodeItem, ProblemItem, CodeTestcaseItem
import json
import scrapy
from redis_database.redis_util import list_push
from database.constants import problem_items_rediskey, submit_items_rediskey, code_items_rediskey, code_testcase_items_rediskey


def item_to_json(item):
    if not isinstance(item, scrapy.Item):
        return None

    obj = {}
    for key in item.keys():
        obj[key] = item[key]
    return json.dumps(obj)


class CodePipeline(object):
    def process_item(self, item, spider):
        if not isinstance(item, CodeItem):
            return item

        json_item = item_to_json(item)
        if json_item:
            list_push(code_items_rediskey, json_item)

        return item


class CodeTestcasePipeline(object):
    def process_item(self, item, spider):
        if not isinstance(item, CodeTestcaseItem):
            return item

        json_item = item_to_json(item)
        if json_item:
            list_push(code_testcase_items_rediskey, json_item)

        return item


class SubmitPipeline(object):
    def process_item(self, item, spider):

        if not isinstance(item, SubmitItem):
            return item

        json_item = item_to_json(item)
        if json_item:
            list_push(submit_items_rediskey, json_item)

        return item


class ProblemPipeline(object):
    def process_item(self, item, spider):

        if not isinstance(item, ProblemItem):
            return item

        json_item = item_to_json(item)
        if json_item:
            list_push(problem_items_rediskey, json_item)

        return item