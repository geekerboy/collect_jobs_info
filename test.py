import collect_jobs
import pandas as pd
import internet

cumt = collect_jobs.university()
cumt.name = 'cumt'
cumt.url = 'http://jyzd.cumt.edu.cn/campus'

page = internet.google_open_web(cumt.url, True)
cumt_xpath = '//*[@id="mn"]/div[2]'

jobs = collect_jobs.get_element_info(page, cumt_xpath)
print(jobs.text)
