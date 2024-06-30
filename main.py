import time
import csv

import client
from db_utils import MoodleDB
from configparser import ConfigParser






def db_to_csv(db):
    """
    数据表转成大模型可以识别的csv文件

    在写了在写了
    :param db:
    :return: csv.reader
    """
    return db


if __name__ == '__main__':
    conf = ConfigParser()
    conf.read('config.ini')
    config = {
        'host': conf['mysql']['host'],
        'port': int(conf['mysql']['port']),
        'database': conf['mysql']['db'],
        'user': conf['mysql']['user'],
        'password': conf['mysql']['password']
    }

    db = MoodleDB(**config)
    old_question_attempts = None
    # 主循环
    while True:
        quesition_attempts = db.get_question_attempts('mdl_question_attempts')
        if old_question_attempts != quesition_attempts:
            unmarked_csv = db_to_csv(quesition_attempts)
            # 大模型服务器地址
            url = "http://127.0.0.1:8000"
            # 发送POST请求
            data = {'question_database': 'CPT',
                    'return_format': 'CSV',
                    'unmarked_csv': unmarked_csv
                    }

            # 拿到打分后的csv文件
            response_csv = client.get_mark(url, data)

            db.mark_question_attempts(0.5, 1)


        time.sleep(10)
        old_question_attempts = quesition_attempts
    db.close()