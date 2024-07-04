import pymysql
import time

"""
mql_question_attempts_steps: 放评分的数据表
mql_question_attempts: 放学生回答的数据表
"""


class MoodleDB:
    def __init__(self, host, port, user, password, database):
        self.db = pymysql.connect(host=host,
                                  port=port,
                                  user=user,
                                  password=password,
                                  database=database,
                                  charset="utf8")

    # 从数据库中获取数据
    def get_question_attempts(self, datasheet='mdl_question_attempts'):

        sql = 'select * from {}'.format(datasheet)
        cursor = self.db.cursor()
        # 执行查询
        cursor.execute(sql)
        # 获取所有记录
        results = cursor.fetchall()
        # 关闭游标和数据库连接，释放资源
        cursor.close()
        return results

    def mark_question_attempts(self, question_id, grade: float, user_id: int):
        """
        批改题目
        :param question_id: 题目的id
        :param grade: 分数百分比 [0, 1]
        :param user_id: 打分人的id
        :return:
        """
        if 0 < grade < 1:
            question_state = 'mangrpartial'
        else:
            question_state = 'mangrright'

        # 获取所有的回答
        question_attempts_steps = self.get_question_attempts('mdl_question_attempt_steps')

        # 获取最后一条记录的id
        datasheet_id = question_attempts_steps[-1][0] + 1

        # 获取当前题目的序号
        count = 0
        for i in question_attempts_steps:
            if i[1] == question_id:
                count += 1
        sequencenumber = count

        # 获取当前时间
        timecreated = int(time.time())

        # 添加一条ai批改的记录(老师端)
        sql = """
        INSERT INTO mdl_question_attempt_steps (id, questionattemptid, sequencenumber, state, fraction, timecreated, userid)
        VALUES ({}, {}, {}, '{}', {}, {}, {})
        """.format(datasheet_id, question_id, sequencenumber, question_state, grade, timecreated, user_id)
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()

        # 修改该题的打分(学生端)
        sql = """
        UPDATE mdl_quiz_attempts
        SET sumgrades = {}
        WHERE uniqueid = {}
        """.format(grade, question_id)
        cursor.execute(sql)
        self.db.commit()
        cursor.close()
    def commit(self):
        self.db.commit()

    def close(self):
        # 关闭游标和数据库连接，释放资源
        self.db.close()



