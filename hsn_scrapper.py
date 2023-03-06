import pandas as pd
import os
import numpy as np
from tqdm.auto import tqdm
from config import selector_paths, selenium_driver, scrapper_config
from utils import utilities

utilities.make_dir('DATA')
utilities.make_csv(os.path.join('DATA','hsn_descp.csv'),['HSN','DESCP'])

def dgcis_scrapper(hsn_code):
    hsn_code = scrapper_config.check_hsn(hsn_code)
    if os.path.isfile(os.path.join('DATA',hsn_code,f'{hsn_code}.csv')):
        hsn_descp_df = pd.read_csv(os.path.join('DATA','hsn_descp.csv'))
        header = hsn_descp_df[hsn_descp_df.HSN == int(hsn_code)]['DESCP'].values[0]
        data_dict = utilities.csv_to_json(os.path.join('DATA',hsn_code,f'{hsn_code}.csv'))
    else:
        driver = selenium_driver.get_driver_object()
        driver.get("https://tradestat.commerce.gov.in/eidb/ecomcntq.asp")
        df = pd.DataFrame()
        try:
            options = selenium_driver.get_select_options(driver,selector_paths.select_box_path)
            header = None
            for opt in tqdm(options):
                driver.get("https://tradestat.commerce.gov.in/eidb/ecomcntq.asp")
                selenium_driver.select_box(driver,selector_paths.select_box_path,opt)
                selenium_driver.input_box(driver,selector_paths.input_box_path,hsn_code)
                selenium_driver.radio_click(driver,selector_paths.radio_button_path)
                selenium_driver.radio_click(driver,selector_paths.submit_button_path)
                if not selenium_driver.check_element_present(driver,selector_paths.no_record_tag_path):
                    if not header:
                        header = selenium_driver.get_text(driver,selector_paths.hsn_descp_path)
                        header = header.strip()
                    tmp = pd.read_html(driver.page_source)
                    tmp = tmp[1].iloc[:,[1,3]]
                    tmp.columns = ['countries'] + list(tmp.columns)[1:]
                    if df.empty:
                        df = tmp.copy()
                    else:
                        df = pd.merge(df,tmp,on='countries',how='outer')
                else:
                    break
            if opt!='2022-2023(Apr-Dec)':
                if opt!='1997-1998':
                    print('Incomplete')
                    for i in options[options.index(opt):]:
                        df[i] = np.nan
                last_rows = ['Total','India\'s Total','%Share']
                df = df.sort_values('countries', key=lambda x: x.isin(last_rows))
                utilities.make_dir(os.path.join('DATA',hsn_code))
                df.to_csv(os.path.join('DATA',hsn_code,f'{hsn_code}.csv'),index=False)
                data_dict = {'HSN': hsn_code, 'DESCP':header}
                utilities.write_csv(os.path.join('DATA','hsn_descp.csv'),data_dict)
                data_dict = utilities.csv_to_json(os.path.join('DATA',hsn_code,f'{hsn_code}.csv'))
            else:
                data_dict = {}
                header = ''
        except Exception as e:
            pass
        driver.stop_client()
        driver.close()
        driver.quit()
    return header,data_dict
        
if __name__ == '__main__':
    hsn_code = ['090831','12345678','0904','0910']
    for i in hsn_code:
        print(i)
        t = dgcis_scrapper(i)
    # print(t[0])
    # print(t[1])