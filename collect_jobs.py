import re
import internet
import normal
import pandas as pd

today = normal.get_time(1, '-')
key_word = ['研究院', '研究所']
saved_path = 'files/' + today + '.xls'


class SearchJob:
    def __init__(self):
        self.url = ''
        self.name = ''
        self.base_xpath = ''
        self.href_suffix = ''
        self.page_suffix = ''
        self.next_page_xpath = ''
        self.res = []
        self.web = None

    def open_web(self):
        return internet.google_open_web(self.url, False)

    def get_current_page(self):
        for i in range(2, 22):
            find_res = None
            xpath = self.base_xpath + '[' + str(i) + ']'
            try:
                find_res = self.web.find_element_by_xpath(xpath)
            except:
                print('加载页面出错,检查网页是否能打开')
                self.web.quit()
                exit()
            for item in key_word:
                if item in find_res.text:
                    # print(find_res.text)
                    tmp_xpath = xpath + self.href_suffix
                    tmp_res = self.web.find_element_by_xpath(tmp_xpath)
                    # print(tmp_res.get_attribute('href'))
                    # 处理数据
                    filter_info = re.findall(r'(.*)[\s\S]', find_res.text)
                    self.res.append(filter_info[0])  # 名称
                    self.res.append(filter_info[2].strip()[:10])  # 发布日期
                    self.res.append(tmp_res.get_attribute('href'))  # 链接

    def get_page(self, num=1):
        for i in range(1, num + 1):
            print('正在搜寻第', i, '/', num, '页内容', sep='')
            self.get_current_page()
            self.web.find_element_by_xpath(self.next_page_xpath).click()

    def show_data(self):
        print(self.res)


class Company:
    def __init__(self):
        self.name = []
        self.date = []
        self.link = []
        self.file_path = ''

    def collect_data(self, res):
        print('正在处理获得数据')
        exist_company = pd.read_excel('files/base.xls')
        for index, item in enumerate(res):
            exist_flag = False
            if index % 3 == 0 and not exist_flag:
                if item not in list(exist_company.iloc[:, 0]):
                    self.name.append(item)
                else:
                    exist_flag = True
            elif index % 3 == 1 and not exist_flag:
                self.date.append(item)
            elif index % 3 == 2 and not exist_flag:
                self.link.append(item)

    def save(self):
        if len(self.name) != 0:
            print('拼接数据中...')
            tmp_excel = pd.concat([pd.DataFrame(self.name), pd.DataFrame(self.date),
                                   pd.DataFrame(self.link)], axis=1, ignore_index=True)
            tmp_excel.columns = ['公司', '发布日期', '链接']
            normal.check_dir('files')
            tmp_excel.to_excel(self.file_path, index=False)
            print("文件保存在:", saved_path, sep='')
        else:
            print('没有新单位出现,数据未保存~')


if __name__ == "__main__":
    print('开始执行程序')

    university = SearchJob()
    university.name = 'south_east'
    university.url = 'http://seu.91job.org.cn/campus/index?keyword=&range=&city=320000&time='
    university.base_xpath = '//*[@id="mn"]/div[2]/ul'
    university.next_page_xpath = '//*[@id="yw1"]/li[13]/a'
    university.href_suffix = '/li[1]/a'
    university.page_suffix = '&page='

    university.web = university.open_web()
    university.get_page(6)  # 改变查找的页数
    # university.show_data()

    # 信息整理
    com = Company()
    com.file_path = saved_path

    com.collect_data(university.res)
    com.save()

    normal.hint(0, '运行结束')
    university.web.quit()
