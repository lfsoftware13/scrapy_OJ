import sqlite3
from database.constants import SUBMIT
from database.database_util import initSubmit, runCommand

find_count = 0

def get_blank_code_submitid(conn, num=100):
    cmd = 'SELECT id FROM '+SUBMIT+' WHERE code = "" ORDER BY ID ASC LIMIT '+str(num)
    #print(cmd)
    global find_count
    find_count += 1
    f = open(r"C:\Users\Lf\Desktop\spider\code_record.txt", 'a')
    f.write("[INFO]["+str(find_count)+"]["+cmd+"]\n")
    print("[INFO]["+str(find_count)+"]["+cmd+"]\n")
    f.close()
    res = runCommand(conn, cmd)
    li = []
    if res:
        li = [r[0] for r in res]
    return li