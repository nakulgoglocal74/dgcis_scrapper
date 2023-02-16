import pandas as pd
import selenium_driver
import os
import json
from tqdm.auto import tqdm

f = open("/home/nakul74/Desktop/scrapper/hsn.json")
hsn_codes = json.load(f)
f.close()

if not os.path.isdir('DGCIS_DATA'):
    os.mkdir('DGCIS_DATA')
    
if not os.path.isfile(os.path.join('DGCIS_DATA','hsn_descp.csv')):
    hsn_descp = pd.DataFrame(columns = ['HSN','DESCP'])
    hsn_descp.to_csv(os.path.join('DGCIS_DATA','hsn_descp.csv'),index=False)


HSN_CODE = '3306'
select_box_path = '#select2'
input_box_path = 'body > div > div.container > div > form > table:nth-child(1) > tbody > tr:nth-child(2) > td:nth-child(2) > p > input'
radio_button_path = '#radiousd'
submit_button_path = '#button1'
hsn_descp_path = 'body > div > div.container > div > font'

hsn_descp = pd.read_csv(os.path.join('DGCIS_DATA','hsn_descp.csv'))
driver = selenium_driver.get_driver_object()

error = []
for HSN_CODE in tqdm(list(hsn_codes.values())):
    if ((len(str(HSN_CODE)) % 2) != 0):
        HSN_CODE = '0' + str(HSN_CODE)
    if not os.path.isfile(os.path.join('DGCIS_DATA',f'{HSN_CODE}.csv')):
        try:
            driver.get("https://tradestat.commerce.gov.in/eidb/ecomcntq.asp")

            df = pd.DataFrame()
            options = selenium_driver.get_select_options(driver,select_box_path)
            header = None
            try:
                for opt in options:
                    driver.get("https://tradestat.commerce.gov.in/eidb/ecomcntq.asp")
                    selenium_driver.select_box(driver,select_box_path,opt)
                    selenium_driver.input_box(driver,input_box_path,HSN_CODE)
                    selenium_driver.radio_click(driver,radio_button_path)
                    selenium_driver.radio_click(driver,submit_button_path)
                    if not header:
                        header = selenium_driver.get_text(driver,hsn_descp_path)
                        header = header.split(':')[1].strip()
                    tmp = pd.read_html(driver.page_source)
                    tmp = tmp[1].iloc[:,[1,3]]
                    tmp.columns = ['countries'] + list(tmp.columns)[1:]
                    if df.empty:
                        df = tmp.copy()
                    else:
                        df = pd.merge(df,tmp,on='countries',how='outer')
            except Exception as e:
                print(e)
                
            last_rows = ['Total','India\'s Total','%Share']
            df = df.sort_values('countries', key=lambda x: x.isin(last_rows))
            df.to_csv(os.path.join('DGCIS_DATA',f'{HSN_CODE}.csv'),index=False)
            
            hsn_header = {'HSN': [HSN_CODE], 'DESCP':[header]}
            hsn_header = pd.DataFrame(hsn_header)
            hsn_descp = pd.concat([hsn_descp, hsn_header], ignore_index = True)
            
        except Exception as e:
            print(e)
            error.append((HSN_CODE,opt))
    
hsn_descp = hsn_descp.reset_index()        
hsn_descp.to_csv(os.path.join('DGCIS_DATA','hsn_descp.csv'),index=False)
print(error)
driver.close()
