from redis_database.redis_util import list_pop, list_push, llendb
from database.constants import code_testcase_start_rediskey, SEMANTIC_TRAIN_DATABASE, PROBLEM_TESTCASE, \
    PROBLEM_TESTCASE_DATABASE

import sqlite3


def read_submit_urls():
    conn = sqlite3.connect(SEMANTIC_TRAIN_DATABASE)
    cur = conn.cursor()
    cmd = "SELECT submit_url FROM cpp_testcase_error_records where distance!=-1 and distance<30"
    cur.execute(cmd)
    res = cur.fetchall()
    urls = [r[0] for r in res]
    return urls


def push_code_testcase_start_urls():
    urls = read_submit_urls()
    print('total urls: {}'.format(len(urls)))
    for url in urls:
        list_push(code_testcase_start_rediskey, 'http://codeforces.com'+url)
    print('finish')


def read_problem_testcase_urls():
    conn = sqlite3.connect(PROBLEM_TESTCASE_DATABASE)
    cur = conn.cursor()
    cmd = "SELECT submit_url FROM problem_testcase where testcase='' or testcase=\"'[]'\""
    cur.execute(cmd)
    res = cur.fetchall()
    urls = [r[0] for r in res]
    return urls


def push_problem_testcase_start_urls():
    urls = read_problem_testcase_urls()
    print('total urls: {}'.format(len(urls)))
    for url in urls:
        list_push(code_testcase_start_rediskey, 'http://codeforces.com'+url)
    print('finish')


if __name__ == '__main__':
    push_problem_testcase_start_urls()
