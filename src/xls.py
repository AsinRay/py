import pandas as pd

filename = r"/home/boot/src/github/conf/github.xls"
df = pd.read_excel(filename, sheet_name=0)
print df.head()
