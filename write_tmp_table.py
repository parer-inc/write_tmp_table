"""This service allows to write new channels to db"""
import os
import sys
import time
import MySQLdb
from rq import Worker, Queue, Connection
from methods.connection import get_redis, get_cursor


def write_tmp_table(data, name):
    """Writes data into tmp table"""
    if "tmp" not in name:
        # log that name was wrong
        return False
    cursor, db = get_cursor()
    q = f'''INSERT INTO  {name}
            (data)
            VALUES
            (%s);'''
    try:
        cursor.executemany(q, data)
    except MySQLdb.Error as error:
        print(error)
        sys.exit("Error:Failed writing new data to db")
    cursor.execute()
    db.commit()
    return True


if __name__ == '__main__':
    time.sleep(5)
    r = get_redis()
    q = Queue('write_tmp_table', connection=r)
    with Connection(r):
        worker = Worker([q], connection=r,  name='write_tmp_table')
        worker.work()
