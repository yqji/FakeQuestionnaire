#coding: utf8

import requests
import re
import time
import random
import numpy as np

class Questionnaire:

    def __init__(self, url):
        self.wj_url = url
        self.post_url = None
        self.header = None
        self.cookie = None
        self.data = None

    def get_ktimes(self):
        return random.randint(5, 18)

    def set_header(self):
        ip = '{}.{}.{}.{}'.format(112, random.randint(64, 68), random.randint(0, 255), random.randint(0, 255))
        self.header = {
            'X-Forwarded-For': ip,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko\
                        ) Chrome/71.0.3578.98 Safari/537.36',
        }

    def get_response(self):
        response = requests.get(url=self.wj_url, headers=self.header)
        self.cookie = response.cookies
        return response

    def get_jqnonce(self, response):
        jqnonce = re.search(r'.{8}-.{4}-.{4}-.{4}-.{12}', response.text)
        return jqnonce.group()

    def get_rn(self, response):
        rn = re.search(r'\d{9,10}\.\d{8}', response.text)
        return rn.group()

    def get_id(self, response):
        id = re.search(r'\d{8}', response.text)
        return id.group()

    def get_jqsign(self, ktimes, jqnonce):
        result = []
        b = ktimes % 10
        if b == 0:
            b = 1
        for char in list(jqnonce):
            f = ord(char) ^ b
            result.append(chr(f))
        return ''.join(result)

    def get_start_time(self, response):
        start_time = re.search(r'\d+?/\d+?/\d+?\s\d+?:\d{2}', response.text)
        return start_time.group()


    def set_post_url(self):
        self.set_header()
        response = self.get_response()
        ktimes = self.get_ktimes()
        jqnonce = self.get_jqnonce(response)
        rn = self.get_rn(response)
        id = self.get_id(response)
        jqsign = self.get_jqsign(ktimes, jqnonce)
        start_time = self.get_start_time(response)
        time_stamp = '{}{}'.format(int(time.time()), random.randint(100, 200))
        url = 'https://www.wjx.cn/joinnew/processjq.ashx?submittype=1&curID={}&t={}&starttim' \
              'e={}&ktimes={}&rn={}&jqnonce={}&jqsign={}'.format(id, time_stamp, start_time, ktimes, rn, jqnonce, jqsign)
        self.post_url = url
        print(self.post_url)

    def set_data(self, data):
        self.data = {
            'submitdata': data
        }

    def post_data(self, data):
        self.set_data(data)
        response = requests.post(url=self.post_url, data=self.data, headers=self.header, cookies=self.cookie)
        return response

    def run(self, data):
        self.set_post_url()
        result = self.post_data(data)
        print(result.content)


    def mul_run(self, n):
        for i in range(n):
            self.run()


def generate_ans(cnt):
        cities = ['上海', '北京', '广州', '深圳', '西安', '太原']
        np.random.seed(0)
        p1 = np.array([0.42, 0.58])
        p2 = np.array([0.01, 0.92, 0.02, 0.05])
        p3 = np.array([0.27, 0.65, 0.05, 0.03])
        p4 = np.array([0.5, 0.1, 0.1, 0.1, 0.1, 0.1])
        p5 = np.array([0.19, 0.81])
        p6 = np.array([0.47, 0.22, 0.21, 0.05, 0.05])
        p7 = np.array([0.30, 0.45, 0.25])
        p8 = np.array([0.03, 0.47, 0.4, 0.1])
        idx1 = np.random.choice(2, p=p1.ravel(), size=cnt)
        idx2 = np.random.choice(4, p=p2.ravel(), size=cnt)
        idx3 = np.random.choice(4, p=p3.ravel(), size=cnt)
        idx4 = np.random.choice(6, p=p4.ravel(), size=cnt)
        idx5 = np.random.choice(2, p=p5.ravel(), size=cnt)
        idx6 = np.random.choice(5, p=p6.ravel(), size=cnt)
        idx7 = np.random.choice(3, p=p7.ravel(), size=cnt)
        idx8 = np.random.choice(4, p=p8.ravel(), size=cnt)

        answers = list()

        for i in range(cnt):
            ans = '1$%d}2$%d}3$%d}4$%s}5$%d}6$%d}7$%d}8$%d' % (idx1[i]+1, idx2[i]+1, idx3[i]+1, cities[idx4[i]], idx5[i]+1, idx6[i]+1, idx7[i]+1, idx8[i]+1)
            answers.append(ans)

        return answers


if __name__ == '__main__':
    w = Questionnaire('https://www.wjx.cn/m/xxxxxx.aspx')
    answers = generate_ans(100)
    for ans in answers:
        w.run(ans)
        time.sleep(random.randint(0,2))









