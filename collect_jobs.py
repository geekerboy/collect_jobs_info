import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import normal
from normal import delay_ms
from normal import align_print
import internet
import time

path_cur = normal.get_current_path()
today = normal.get_time(1, '-')
file_save_path = 'files'


def get_element_info(website, xpath):
    delay_ms(160)
    try:
        ele = WebDriverWait(website, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
    except:
        print('加载页面出错')
    return ele


class company:
    def __init__(self):
        self.name = []
        self.date = []
        self.talk_time = []
        self.adress = []

    def add_suffix(self, suffix):
        self.name.append(suffix)
        self.date.append(suffix)
        self.talk_time.append(suffix)
        self.adress.append(suffix)


class university:
    def __init__(self):
        self.url = ''
        self.name = ''

    def get_file_path(self):
        file_path = path_cur + '/' + file_save_path + '/' + today + '-' + self.name + '.xls'
        return file_path

    def finish_job(self):
        print(self.name, 'university数据获取完成~')


if __name__ == '__main__':
    start = time.time()

    southeast = university()
    southeast.name = 'southeast'
    southeast.url = 'http://seu.91job.org.cn/'

    nanjing_url = 'http://job.nju.edu.cn/#!/more/special_recruit'
    nuaa_url = 'http://job.nuaa.edu.cn/jobfair'
    njust_url = 'http://njust.91job.org.cn/jobfair'

    page = internet.google_open_web(southeast.url)
    recruitment_talk_xpath = '/html/body/div[1]/div[3]/div[2]/div/div[3]/div[2]/ul[1]'
    chuiniu = get_element_info(page, recruitment_talk_xpath)
    second_time = time.time()
    print('打开网页耗时：', second_time - start, 's', sep='')
    # print(chuiniu.text)

    align_print('开始筛选数据')
    third_time = time.time()
    all_data = re.findall(r'(.*)[\s\S]', chuiniu.text)
    print(all_data)
    fouth_time = time.time()
    print('筛选数据耗时：', fouth_time - third_time, 's', sep='')

    align_print('筛选完成,正在处理')
    all_company = company()
    for index, data in enumerate(all_data):
        position = index % 7
        if position == 0:
            tmp_data = data + all_data[index + 1]
            all_company.date.append(tmp_data)
        elif position == 2:
            all_company.name.append(data)
        elif position == 4:
            all_company.talk_time.append(data)
        elif position == 5:
            all_company.adress.append(data)
    all_company.add_suffix(southeast.name)
    tmp_excel = pd.concat([pd.DataFrame(all_company.name), pd.DataFrame(all_company.date),
                           pd.DataFrame(all_company.talk_time), pd.DataFrame(all_company.adress)
                           ], axis=1, ignore_index=True)
    tmp_excel.columns = ['公司', '举办日期', '时间', '地点']
    normal.check_dir('files')
    tmp_excel.to_excel(southeast.get_file_path(), index=False)
    southeast.finish_job()
    # 筛选日期
    # date = re.findall(r'\d{2}[\u4e00-\u9fa5][\s\S]\d{2}[\u4e00-\u9fa5]', chuiniu.text)
    # for index, data in enumerate(date):
    #     date[index] = data.replace('\n', '')
    # print(date)

    # 筛选时间
    # talk_time = re.findall(r'\d{2}:\d{2}-\d{2}:\d{2}', chuiniu.text)
    # print(talk_time)
    page.quit()
# ^ 匹配字符串的开始。
# $ 匹配字符串的结尾。
# \b 匹配一个单词的边界。
# \d 匹配任意数字。
# \D 匹配任意非数字字符。
# x? 匹配一个可选的 x 字符 (换言之，它匹配 1 次或者 0 次 x 字符)。
# x* 匹配0次或者多次 x 字符。
# x+ 匹配1次或者多次 x 字符。
# x{n,m} 匹配 x 字符，至少 n 次，至多 m 次。
# (a|b|c) 要么匹配 a，要么匹配 b，要么匹配 c。
# (x) 一般情况下表示一个记忆组 (remembered group)。你可以利用 re.search
# 函数返回对象的 groups() 函数获取它的值。
# 正则表达式中的点号通常意味着 “匹配任意单字符”
