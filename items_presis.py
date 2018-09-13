from redis_database.redis_util import list_pop, list_push, llendb
from database.database_util import insertSubmit, insertCode, runCommand, find, insertProblem, initSubmit, insertSubmitMany, findIdExist, insertCodeMany, insertCodeTestcaseMany
from database.constants import SUBMIT, DATABASE_PATH, problem_items_rediskey, submit_items_rediskey, code_items_rediskey, code_notexist_items_rediskey, code_testcase_items_rediskey
import json
import logging
from util.ScriptsUtil import initLogging, convert_to_itemlist_ordered
import time
import os

def presis_submit(conn, sub_json):
    sub_obj = json.loads(sub_json)

    for ke in sub_obj.keys():
        if len(sub_obj[ke]) > 0:
            sub_obj[ke] = sub_obj[ke][0]
        elif len(sub_obj[ke]) <= 0:
            sub_obj[ke] = ''

    pro_name = ''
    name_list = sub_obj['problem_full_name'].split(' ')
    if len(name_list) > 0:
        pro_name = name_list[0]

    insertSubmit(conn, sub_obj['id'], sub_obj['submit_url'], sub_obj['submit_time'], sub_obj['user_id']
                 , sub_obj['user_name'], sub_obj['problem_id'], sub_obj['problem_url'], pro_name, sub_obj['problem_full_name']
                 , sub_obj['language'], sub_obj['status'], sub_obj['error_test_id'], sub_obj['time']
                 , sub_obj['memory'])
    logging.info("[PRESISTENT][SUBMIT]["+sub_json+"]")
    return 1

def presis_submit_many():
    cou = 0
    sub_list = []
    for i in range(0, 1000):
        sub = list_pop(submit_items_rediskey)
        if sub:
            cou += 1
            sub_obj = json.loads(str(sub, encoding="utf-8"))
            sub_item = convert_to_itemlist_ordered(sub_obj)
            sub_list.append(sub_item)

    if len(sub_list) > 0:
        insertSubmitMany(sub_list)
        logging.info("[PRESISTENT][SUBMIT MANY]["+str(cou)+"]")
    return 1

def presis_code(conn, code_json):
    code_obj = json.loads(code_json)

    id = code_obj['id']
    code = code_obj['code']
#    res = find(conn, SUBMIT, 'id', id)
    if len(find(conn, SUBMIT, 'id', id)) > 0:
        logging.info("[PRESISTENT][CODE][" + code_obj['id'] + "]")
        insertCode(conn, id, code)
        return 1
    logging.info("[NOTEXIST][CODE][" + code_obj['id'] + "]")
    return 0

def presis_code_many():

    cod_list = []
    ids = []
    for i in range(0, 1000):
        cod = list_pop(code_items_rediskey)
        if cod:
            cod_obj = json.loads(str(cod, encoding="utf-8"))
            cod_list.append(cod_obj)
            ids.append(cod_obj['id'])

    exi_res = findIdExist(ids, SUBMIT, 'id')
    exist_ids = []
    for e in exi_res:
        exist_ids.append(e[0])

    cou_exi = 0
    cou_nexi = 0
    update_list = []
    for c in cod_list:
        if c['id'] not in exist_ids:
            cou_nexi += 1
            list_push(code_notexist_items_rediskey, json.dumps(c))
        else:
            cou_exi += 1
            update_list.append(c)

    if len(update_list) > 0:
        insertCodeMany(update_list)
        logging.info("[PRESISTENT][CODE MANY][UPDATE "+str(cou_exi)+" CODE ITEMS][REPUSH "+str(cou_nexi)+" CODE ITEMS]")
    else:
        logging.info("[PRESISTENT][CODE MANY][UPDATE NOTHING]")
    return 1


def presis_code_testcase_many():

    cod_list = []
    ids = []
    for i in range(0, 1000):
        cod = list_pop(code_testcase_items_rediskey)
        if cod:
            cod_obj = json.loads(str(cod, encoding="utf-8"))
            cod_obj['testcase'] = json.dumps(cod_obj['testcase'])
            cod_list.append(cod_obj)
            ids.append(cod_obj['id'])

    # exi_res = findIdExist(ids, SUBMIT, 'id')
    # exist_ids = []
    # for e in exi_res:
    #     exist_ids.append(e[0])

    cou_exi = 0
    cou_nexi = 0
    update_list = []
    for c in cod_list:
        # if c['id'] not in exist_ids:
        #     cou_nexi += 1
        #     list_push(code_notexist_items_rediskey, json.dumps(c))
        # else:
            cou_exi += 1
            update_list.append(c)

    if len(update_list) > 0:
        insertCodeTestcaseMany(update_list)
        # print('ids: ', ids)
        logging.info("[PRESISTENT][CODE TESTCASE MANY][UPDATE "+str(cou_exi)+" CODE TESTCASE ITEMS][REPUSH "+str(cou_nexi)+" CODE ITEMS]")
    else:
        logging.info("[PRESISTENT][CODE TESTCASE MANY][UPDATE NOTHING]")
    return 1


def presis_problem(conn, pro_json):
    pro_obj = json.loads(pro_json)

    tags = pro_obj['tags']
    tag_str = ''
    isF = 1
    for ta in tags:
        if not isF:
            tag_str += ':'
        isF = 0
        tag_str += ta

    for ke in pro_obj.keys():
        if len(pro_obj[ke]) > 0:
            if ke != 'tags':
                pro_obj[ke] = pro_obj[ke][0]
        elif len(pro_obj[ke]) <= 0:
            pro_obj[ke] = ''

    insertProblem(conn, pro_obj['problem_name'], pro_obj['problem_url'], pro_obj['problem_des_name'], tag_str, pro_obj['submit_urls'])
    logging.info("[PRESISTENT][PROBLEM][" + pro_json + "]")
    return 1

def presis(conn):
    cou_pro = 0
    cou_sub = 0
    cou_cod = 0

    exi = list_pop(code_notexist_items_rediskey)
    while exi:
        list_push(code_items_rediskey, exi)
        exi = list_pop(code_notexist_items_rediskey)

    pro = list_pop(problem_items_rediskey)
    while pro:
        cou_pro += 1
        pro_str = str(pro, encoding="utf-8")
        presis_problem(conn, pro_str)
        pro = list_pop(problem_items_rediskey)

    while llendb(submit_items_rediskey) > 100:
        presis_submit_many()

    while llendb(code_items_rediskey) > 50:
        presis_code_many()

    logging.info('[PRESISTENCE FINISH. PRESISTENT '+str(cou_pro)+' PROBLEM. PRESISTENT '+str(cou_sub)+' SUBMIT. PRESISTENT '+str(cou_cod)+' CODE.]')

def main():
    initLogging()
    os.chdir('/home/lf/DataCrawl/scrapy_OJ/')
    conn = None
    logging.info('[Item Presistence start success]')
    presis(conn)


def main_testcase():
    initLogging()
    os.chdir('/home/lf/DataCrawl/scrapy_OJ/')
    while llendb(code_testcase_items_rediskey) > 0:
        presis_code_testcase_many()

if __name__ == '__main__':
    main_testcase()

