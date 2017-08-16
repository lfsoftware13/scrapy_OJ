import sqlite3
from database.constants import DATABASE_PATH, SUBMIT, PROBLEM


def initSubmit():
    conn = sqlite3.connect(DATABASE_PATH)
    checkExist(conn)
    return conn


def close(conn):
    conn.close()


def checkExist(conn):
    com = '''CREATE TABLE IF NOT EXISTS '''+SUBMIT+'''
    (id TEXT primary key,
    submit_url TEXT,
    submit_time TEXT,
    user_id TEXT,
    user_name TEXT,
    problem_id TEXT,
    problem_url TEXT,
    problem_name TEXT,
    problem_full_name TEXT,
    language TEXT,
    status TEXT,
    error_test_id TEXT,
    time TEXT,
    memory TEXT,
    code TEXT)'''
    conn.execute(com)
    conn.commit()

    com = '''CREATE TABLE IF NOT EXISTS '''+PROBLEM+'''
    (problem_name TEXT primary key,
    problem_url TEXT,
    problem_des_name TEXT,
    tags TEXT,
    submit_urls TEXT)'''
    conn.execute(com)
    conn.commit()

def insertSubmit(conn, id, submit_url, submit_time, user_id, user_name, problem_id, problem_url, problem_name, problem_full_name,language, status, error_test_id, time, memory):
    if not conn:
        conn = initSubmit()

    cmd = 'INSERT OR IGNORE INTO submit (id, submit_url, submit_time, user_id, user_name, problem_id, problem_url, problem_name, problem_full_name, language, status, error_test_id, time, memory, code) ' \
          'VALUES ("'+id+'", "'+submit_url+'", "'+submit_time+'", "'+user_id+'", "'+user_name+'", "'+problem_id+'", "'+problem_url+'", "'+problem_name+'", "'+problem_full_name+'", "'+language+'", "'+status+'", ' \
          '"'+error_test_id+'", "'+time+'", "'+memory+'", "")'
    conn.execute(cmd)
    conn.commit()

def insertCode(conn, id, code):
    if not conn:
        conn = initSubmit()

    code = code.replace("'", "''")
    cmd = "UPDATE submit SET code = '''"+code+"''' WHERE id = '"+id+"' "
    conn.execute(cmd)
    conn.commit()

def insertProblem(conn, problem_name, problem_url, problem_des_name, tags, submit_urls):
    if not conn:
        conn = initSubmit()

    cmd = 'INSERT OR IGNORE INTO problem (problem_name, problem_url, problem_des_name, tags, submit_urls) ' \
          'VALUES ("'+problem_name+'", "'+problem_url+'", "'+problem_des_name+'", "'+tags+'", "'+submit_urls+'")'
    conn.execute(cmd)
    conn.commit()

def find(conn, table_name, key, value):
    if not conn:
        conn = initSubmit()

    cmd = "SELECT * FROM "+table_name+" WHERE "+key+"='"+value+"' "
    cur = conn.execute(cmd)
    return cur.fetchall()

def runCommand(conn, cmd):
    if not conn:
        conn = initSubmit()

    return conn.execute(cmd)