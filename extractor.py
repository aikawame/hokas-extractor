import os
import pandas
import sqlite3
import urllib.request
import camelot
import settings

dfs = []
for filename in settings.pdf_filenames:
    remote_url = settings.pdf_url + filename
    local_path = settings.temp_dir + filename
    if not os.path.exists(local_path):
        print('Downloading PDF:', remote_url)
        urllib.request.urlretrieve(remote_url, local_path)
    print('Extracting PDF:', local_path)
    dfs.append(pandas.concat([table.df for table in camelot.read_pdf(local_path, pages='all', split_text=True)]))

df = pandas.concat(dfs)
df.columns = ['name', 'type', 'description', 'ref']
df.set_index('name', inplace=True)
df.type = df.type.str.replace(' ', '')  # 区分にレイアウト用の半角スペースが混じっているので消す
df = df[df.type != '']  # 索引行を消す
df = df[df.type != '区分']  # 見出し行を消す
df.replace('\n', '', regex=True, inplace=True)  # レイアウト用の改行を除去する

output_path = settings.dist_dir + settings.output_filename
if os.path.isfile(output_path):
    os.remove(output_path)
conn = sqlite3.connect(output_path)
df.to_sql('items', conn)
conn.close()
