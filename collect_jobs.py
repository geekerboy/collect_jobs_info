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
    web_flag = 0

    def __init__(self):
        self.url = ''
        self.name = ''
        self.xpath = ''
        self.index = 0

    def get_file_path(self):
        file_path = path_cur + '/' + file_save_path + '/' + today + '-' + self.name + '.xls'
        return file_path

    def get_origin_text(self, window=False, web=None):
        university.web_flag += 1
        self.index = university.web_flag
        web_msg=self.name+'网页访问成功,正在获取内容'
        if university.web_flag < 2:
            webpage = internet.google_open_web(self.url, window)
            delay_ms(20)
            align_print(web_msg)
            ele = WebDriverWait(webpage, 10).until(EC.presence_of_element_located((By.XPATH, self.xpath)))
        else:
            url = 'window.open("' + self.url + '");'
            web.execute_script(url)
            # 当前句柄还在上一个
            handles = web.window_handles
            web.switch_to_window(handles[self.index - 1])
            delay_ms(20)
            align_print(web_msg)
            ele = WebDriverWait(web, 10).until(EC.presence_of_element_located((By.XPATH, self.xpath)))
        # try:
        #     ele = WebDriverWait(webpage, 10).until(
        #         EC.presence_of_element_located((By.XPATH, self.xpath)))
        # except:
        #     print('加载页面出错')
        # 两空格之间内容挑出来
        filiter_info = re.findall(r'(.*)[\s\S]', ele.text)
        align_print('内容获取完毕,正在进行数据处理')
        if university.web_flag < 2:
            return webpage, filiter_info
        else:
            return filiter_info

    def finish_job(self):
        print(self.name, 'university数据获取完成~')


if __name__ == '__main__':
    align_print('程序已启动')
    southeast = university()
    southeast.name = 'southeast'
    southeast.url = 'http://seu.91job.org.cn/'
    southeast.xpath = '/html/body/div[1]/div[3]/div[2]/div/div[3]/div[2]/ul[1]'

    nanjing_url = 'http://job.nju.edu.cn/#!/more/special_recruit'
    nuaa_url = 'http://job.nuaa.edu.cn/jobfair'
    njust_url = 'http://njust.91job.org.cn/jobfair'

    webpage, all_data = southeast.get_origin_text()
    # print(all_data)

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
    webpage.quit()
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
