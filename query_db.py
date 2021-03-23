import psycopg2
import datetime


def get_timedelta(id):
    """ an id is fetched from database to return a tuple from which a timedelta is extracted """

    conn = psycopg2.connect(
        dbname="todo_app", user="postgres", password="1234")

    cur = conn.cursor()

    id = str(id)

    cur.execute(
        "SELECT AGE(finished, started) FROM todo_list WHERE id=%s", (id,))

    a_task = cur.fetchone()

    cur.close()

    conn.close()

    return a_task[0]

# get_timedelta(1)
# print(get_timedelta(1))
