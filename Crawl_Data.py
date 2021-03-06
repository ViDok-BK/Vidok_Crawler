#from General_Code import gen_code
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support.ui import Select
import os



def get_data():
    # Đường dẫn đến thư mục chưa các file được download
    current_dir = os.getcwd()
    path_save = current_dir + "/complex_ligand"

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    prefs = {"download.default_directory" : path_save, 'profile.default_content_setting_values.automatic_downloads': 1}
    options.add_experimental_option("prefs",prefs)

    # Đường dẫn đến file chromedriver
    browser = webdriver.Chrome(executable_path=current_dir + '/chromedriver',   chrome_options = options)
    browser.get('https://vidok.chpc.utah.edu/web.top.all.time.php')

    select  = Select(browser.find_element_by_xpath('//*[@id="rs_tbl_length"]/label/select'))
    select.select_by_value('500')

    link_ligand = []

    for _ in range(2):
        # browser.find_element_by_xpath('//*[@id="rs_tbl_next"]/a').click()
        for i in range(1,501):
            link_page_ligand = browser.find_element_by_xpath('//*[@id="rs_tbl"]/tbody/tr[{}]/td[6]/a[1]'.format(str(i))).get_attribute('href')
            link_ligand.append(link_page_ligand)
        browser.find_element_by_xpath('//*[@id="rs_tbl_next"]/a').click()

    i = 1

    for link in link_ligand:
        browser.execute_script("window.open('');")
        browser.switch_to.window(browser.window_handles[1])
        browser.get(link)

        # Download file pdbqt
        select  = Select(browser.find_element_by_xpath('//*[@id="select_file_2_download_"]'))
        select.select_by_index(3)

        # Download file sdf
        select  = Select(browser.find_element_by_xpath('//*[@id="select_file_2_download_"]'))
        select.select_by_index(4)

        # Lấy tên của ligand
        name = browser.find_element_by_xpath('/html/body/div/div[4]/div[2]/div[4]/div').text
        name = name.split('\n')[2].split(' ')[2]
        time.sleep(5)

        print("STT: {} File name: {}".format(i,name))
        i+=1

        # Đổi tên file sdf
        old_name = "{}/ligand_{}.sdf".format(path_save,name)
        new_name = "{}/{}.sdf".format(path_save,name)

        check = True
        while check:
            try:
                os.rename(old_name, new_name)
                check = False
            except Exception as e:
                check = True

        # Đổi tên file pdbqt
        old_name = "{}/receptor-ligand-complex.pdbqt".format(path_save)
        new_name = "{}/{}.pdbqt".format(path_save,name)
        

        check = True
        while check:
            try:
                os.rename(old_name, new_name)
                check = False
            except Exception as e:
                check = True
        

        browser.close()
        browser.switch_to.window(browser.window_handles[0])

    
