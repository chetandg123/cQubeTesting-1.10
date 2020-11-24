import os
import time

from selenium.webdriver.support.select import Select

from Data.parameters import Data
from get_dir import pwd
from reuse_func import GetData


class Check_with_all_clusters():
    def __init__(self ,driver):
        self.driver = driver

    def test_clusters_selectbox(self):
        self.driver.implicitly_wait(100)
        self.data = GetData()
        self.p = pwd()
        count = 0
        self.driver.find_element_by_xpath(Data.hyper_link).click()
        self.data.page_loading(self.driver)
        districts = Select(self.driver.find_element_by_id(Data.sar_district))
        blocks = Select(self.driver.find_element_by_id(Data.sar_block))
        clusters = Select(self.driver.find_element_by_id(Data.sar_cluster))
        collections =Select(self.driver.find_element_by_id(Data.coll_names))
        coll_count = len(collections.options) - 1
        for i in range(len(districts.options)-1,len(districts.options)):
            districts.select_by_index(i)
            self.data.page_loading(self.driver)
            for j in range(len(blocks.options)-1,len(blocks.options)):
                blocks.select_by_index(j)
                self.data.page_loading(self.driver)
                for k in range(1, len(clusters.options)):
                    clusters.select_by_index(k)
                    name = clusters.options[k].text
                    cname=name.strip()
                    self.data.page_loading(self.driver)
                    self.driver.find_element_by_id(Data.Download).click()
                    time.sleep(3)
                    self.filename = self.p.get_download_dir() + "/TPD_data_of_cluster_"+cname.replace(' ','_')+".csv"
                    if os.path.isfile(self.filename) != True:
                        print(districts.options[i].text,blocks.options[j].text,clusters.options[k].text,'csv file is not downloaded')
                        count = count + 1
                    os.remove(self.filename)
                    self.data.page_loading(self.driver)
                    # for m in range(len(collections.options) - 2, len(collections.options)):
                    #     collections.select_by_index(m)
                    #     self.data.page_loading(self.driver)
        return count, coll_count

