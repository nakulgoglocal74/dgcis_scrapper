import os
import pandas as pd
data_folders = os.listdir('DATA')
data_folders = list(filter(lambda x:'.csv' not in x,data_folders))
data_files_paths = []
for i in data_folders:
    file_path = os.path.join('DATA',i,os.listdir(os.path.join('DATA',i))[0])
    data_files_paths.append(file_path)

hsn_descp_file_path = os.path.join('DATA','hsn_descp.csv')
# print(data_files_paths,hsn_descp_file_path)

df = pd.DataFrame()
for i in data_files_paths:
    hsn_code = os.path.basename(i).split('.')[0]
    tmp = pd.read_csv(i)
    tmp.insert(loc=0, column='HSN', value=[hsn_code]*len(tmp))
    tmp['HSN'] = hsn_code
    df = pd.concat([df,tmp])
df = df.reset_index(drop=True)
df.to_csv(os.path.join('DATA','dgcis_all_hsn_data.csv'),index=False)
    