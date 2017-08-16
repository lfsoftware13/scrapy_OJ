from collections import Counter
import sqlite3

conn = sqlite3.connect("data/scrapyOJ.db")
res = conn.execute("SELECT code FROM submit where code <> ''")
code_list = []
t = 0
for r in res:
    t += 1
    code_list.append(r[0])
print(t)

count_list = Counter(code_list)

count = {}
for key, value in count_list.items():
    if value not in count:
        count[value] = 0
    count[value] += 1

print(count)