import pandas as pd
import selenium_driver
import os

if not os.path.isdir('DGCIS_DATA'):
    os.mkdir('DGCIS_DATA')

HSN_CODE = '3306'
select_box_path = '#select2'
input_box_path = 'body > div > div.container > div > form > table:nth-child(1) > tbody > tr:nth-child(2) > td:nth-child(2) > p > input'
radio_button_path = '#radiousd'
submit_button_path = '#button1'

driver = selenium_driver.get_driver_object()
driver.get("https://tradestat.commerce.gov.in/eidb/ecomcntq.asp")

df = pd.DataFrame()
options = selenium_driver.get_select_options(driver,select_box_path)

for opt in options:
    driver.get("https://tradestat.commerce.gov.in/eidb/ecomcntq.asp")
    selenium_driver.select_box(driver,select_box_path,opt)
    selenium_driver.input_box(driver,input_box_path,HSN_CODE)
    selenium_driver.radio_click(driver,radio_button_path)
    selenium_driver.radio_click(driver,submit_button_path)
    tmp = pd.read_html(driver.page_source)
    tmp = tmp[1].iloc[:,[1,3]]
    tmp.columns = ['countries'] + list(tmp.columns)[1:]
    if df.empty:
        df = tmp.copy()
    else:
        df = pd.merge(df,tmp,on='countries',how='outer')

last_rows = ['Total','India\'s Total','%Share']
df = df.sort_values('countries', key=lambda x: x.isin(last_rows))
df.to_csv(os.path.join('DGCIS_DATA',f'{HSN_CODE}.csv'),index=False)

driver.stop_client()
driver.close()
driver.quit()
