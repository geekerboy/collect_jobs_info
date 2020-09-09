import collect_jobs
import pandas as pd
import internet
import re

exist_company = pd.read_excel('files/base.xls')
print(list(exist_company.iloc[:, 0]))
