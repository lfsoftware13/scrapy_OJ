from redis_database.redis_util import list_pop, list_push
from database.database_util import insertSubmit, insertCode, runCommand, find, insertProblem, initSubmit
from database.constants import SUBMIT, DATABASE_PATH, problem_items_rediskey, submit_items_rediskey, code_items_rediskey, code_notexist_items_rediskey
import json
import time
import logging
from util.ScriptsUtil import initLogging
import sqlite3

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

def presis_code(conn, code_json):
    code_obj = json.loads(code_json)

    id = code_obj['id']
    code = code_obj['code']
    res = find(conn, SUBMIT, 'id', id)
    if len(find(conn, SUBMIT, 'id', id)) > 0:
        logging.info("[PRESISTENT][CODE][" + code_obj['id'] + "]")
        insertCode(conn, id, code)
        return 1
    logging.info("[NOTEXIST][CODE][" + code_obj['id'] + "]")
    return 0

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

    sub = list_pop(submit_items_rediskey)
    while sub:
        cou_sub += 1
        sub_str = str(sub, encoding="utf-8")
        presis_submit(conn, sub_str)
        sub = list_pop(submit_items_rediskey)

    cod = list_pop(code_items_rediskey)
    while cod:
        cod_str = str(cod, encoding="utf-8")
        if presis_code(conn, cod_str) == 0:
            list_push(code_notexist_items_rediskey, cod_str)
        else:
            cou_cod += 1
        cod = list_pop(code_items_rediskey)

    logging.info('[TURN][PRESISTENCE FINISH. PRESISTENT '+str(cou_pro)+' PROBLEM. PRESISTENT '+str(cou_sub)+' SUBMIT. PRESISTENT '+str(cou_cod)+' CODE.]')


def main():
    initLogging()
    conn = initSubmit()
    while True:
        presis(conn)
        time.sleep(3600)


main()
