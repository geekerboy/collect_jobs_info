import collect_jobs
import pandas as pd
import internet
import re

cumt = collect_jobs.university()
cumt.name = 'cumt'
cumt.url = 'http://jyzd.cumt.edu.cn/campus'
cumt.xpath = '//*[@id="mn"]/div[2]'

webpage, filiter_info = cumt.get_origin_text(True)
del filiter_info[0:3]
filiter_info.pop()
print(filiter_info)
print('开启下一网页')

southeast = collect_jobs.university()
southeast.name = 'southeast'
southeast.url = 'http://seu.91job.org.cn/'
southeast.xpath = '/html/body/div[1]/div[3]/div[2]/div/div[3]/div[2]/ul[1]'
origin_text = southeast.get_origin_text(False, webpage)
print(origin_text)

webpage.quit()
