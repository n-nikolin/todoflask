import psycopg2
import datetime

conn = psycopg2.connect(dbname="todo_app", user="postgres", password="1234")

cur = conn.cursor()

id = str(id)

cur.execute(
    "SELECT AGE(finished, started) FROM todo_list")

# print(cur.fetchone())
a_task = cur.fetchall()

cur.close()

conn.close()

for task in a_task:
    print(task[0])
# get_timedelta(1)