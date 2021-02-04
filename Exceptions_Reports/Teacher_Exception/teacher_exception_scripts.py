import csv
import os
import re
import time

from selenium.webdriver.support.select import Select

from Data.parameters import Data
from filenames import file_extention
from get_dir import pwd
from reuse_func import GetData


class teacher_exception_report():

    def __init__(self,driver,year,month):
        self.driver = driver
        self.filename =''
        self.year = year.strip()
        self.month = month.strip()

    def test_icon(self):
        self.data = GetData()
        count = 0
        self.driver.find_element_by_xpath(Data.hyper_link).click()
        self.data.page_loading(self.driver)
        self.driver.find_element_by_id('homeBtn').click()
        self.data.page_loading(self.driver)
        self.driver.find_element_by_id('tarExp').click()
        self.data.page_loading(self.driver)
        if "teacher-attendance-exception" in self.driver.current_url:
            print("Teacher exception report page is dispayed")
        else:
            print("Teacher exception icon is not working")
            count = count + 1
        return count


    def click_on_logout(self):
        self.driver.find_element_by_id(Data.Logout).click()
        return self.driver.title

    def test_click_on_dashboard(self):
        count = 0
        cal = GetData()
        self.driver.find_element_by_xpath(Data.hyper_link).click()
        cal.page_loading(self.driver)
        self.driver.find_element_by_id(Data.home).click()
        cal.page_loading(self.driver)
        cal.navigate_to_teacher_exception()
        cal.page_loading(self.driver)
        if 'teacher-attendance-exception' in self.driver.current_url:
            print("Teacher exception report is present ")
        else:
            print("Teacher exception is not exist")
            count = count + 1
        return count

    def test_total_not_recieved_data(self):
        cal = GetData()
        self.driver.find_element_by_xpath(Data.hyper_link).click()
        cal.page_loading(self.driver)

        school_not_recived = self.driver.find_element_by_id('students').text
        notcount = re.sub("\D", "",school_not_recived)

        self.driver.find_element_by_xpath(Data.hyper_link).click()
        self.driver.find_element_by_id('allBlock').click()
        cal.page_loading(self.driver)
        blockcount = self.driver.find_element_by_id('students').text
        bcount = re.sub("\D", "",blockcount)
        cal.page_loading(self.driver)

        self.driver.find_element_by_id('allCluster').click()
        cal.page_loading(self.driver)
        clustcount = self.driver.find_element_by_id('students').text
        clustercount = re.sub("\D", "", clustcount)
        cal.page_loading(self.driver)

        self.driver.find_element_by_id('allSchool').click()
        cal.page_loading(self.driver)
        sccount = self.driver.find_element_by_id('students').text
        schoolcount = re.sub("\D", "", sccount)
        cal.page_loading(self.driver)

        return  notcount , bcount , clustercount,schoolcount

    def check_dots_on_each_districts(self):
        cal = GetData()
        cal.click_on_state(self.driver)
        cal.page_loading(self.driver)
        select_district = Select(self.driver.find_element_by_id('choose_dist'))
        count = 0
        for x in range(1, len(select_district.options)):
            time.sleep(2)
            select_district.select_by_index(x)
            cal.page_loading(self.driver)
            dots = self.driver.find_elements_by_class_name(Data.dots)
            if int(len(dots) - 1) == 0:
                print("District" + select_district.first_selected_option.text + "Markers are not found")
                count = count + 1
        return count

    def check_districts_csv_download(self):
        cal = GetData()
        self.fname = file_extention()
        cal.click_on_state(self.driver)
        cal.page_loading(self.driver)
        select_district = Select(self.driver.find_element_by_id('choose_dist'))
        count = 0
        for x in range(1, len(select_district.options)):
            select_district.select_by_index(x)
            cal.page_loading(self.driver)
            markers = self.driver.find_elements_by_class_name(Data.dots)
            time.sleep(3)
            if (len(markers) - 1) == 0:
                print("District" + select_district.first_selected_option.text + "no data")
                count = count + 1
            else:
                time.sleep(2)
                self.driver.find_element_by_id('download').click()
                time.sleep(2)
                p = pwd()
                self.filename = p.get_download_dir() + "/" + "Block_per_district_report_"+self.month+"_"+self.year+".csv"
                print(self.filename)
                if os.path.isfile(self.filename) != True:
                    return "File Not Downloaded"
                else:
                    with open(self.filename) as fin:
                        csv_reader = csv.reader(fin, delimiter=',')
                        header = next(csv_reader)
                        schools = 0
                        teacher = 0
                        for row in csv.reader(fin):
                            # schools += int(row[6])
                            teacher += int(row[4])
                        teach = self.driver.find_element_by_id("students").text
                        ta = re.sub('\D', "", teach)

                        if int(teacher) != int(ta):
                            print("school count mismatched", int(teacher), int(ta))
                            count = count + 1
                    os.remove(self.filename)
                return markers, count


    def ClusterPerBlockCsvDownload(self):
        cal = GetData()
        self.fname = file_extention()
        cal.click_on_state(self.driver)
        cal.page_loading(self.driver)
        select_district = Select(self.driver.find_element_by_id('choose_dist'))
        select_block = Select(self.driver.find_element_by_id('choose_block'))
        count = 0
        for x in range(len(select_district.options) - 1, len(select_district.options)):
            select_district.select_by_index(x)
            cal.page_loading(self.driver)
            for y in range(1, len(select_block.options)):
                select_block.select_by_index(y)
                cal.page_loading(self.driver)
                time.sleep(2)
                dots = self.driver.find_elements_by_class_name(Data.dots)
                markers= len(dots)-1
                self.driver.find_element_by_id('download').click()
                time.sleep(4)
                p = pwd()
                self.filename = p.get_download_dir() + "/" + "Cluster_per_block_report_"+self.month+"_"+self.year+".csv"
                print(self.filename)
                if os.path.isfile(self.filename) != True:
                    return "File Not Downloaded"
                else:
                    with open(self.filename) as fin:
                        csv_reader = csv.reader(fin, delimiter=',')
                        header = next(csv_reader)
                        teacher = 0
                        for row in csv.reader(fin):
                            teacher += int(row[6])

                        teach = self.driver.find_element_by_id("students").text
                        ta = re.sub('\D', "", teach)

                        if int(teacher) != int(ta):
                            print("Teacher count mismatched", int(teacher), int(ta))
                            count = count + 1
                    os.remove(self.filename)
                return markers, count

    def SchoolPerClusterCsvDownload(self):
        cal = GetData()
        self.fname = file_extention()
        cal.click_on_state(self.driver)
        cal.page_loading(self.driver)
        select_district = Select(self.driver.find_element_by_id('choose_dist'))
        select_block = Select(self.driver.find_element_by_id('choose_block'))
        select_cluster=Select(self.driver.find_element_by_id('choose_cluster'))
        count = 0
        for x in range(len(select_district.options)-1, len(select_district.options)):
            select_district.select_by_index(x)
            cal.page_loading(self.driver)
            for y in range(1, len(select_block.options)):
                time.sleep(2)
                select_block.select_by_index(y)
                cal.page_loading(self.driver)
                for z in range(1,len(select_cluster.options)):
                    select_cluster.select_by_index(z)
                    cal.page_loading(self.driver)
                    time.sleep(2)
                    dots = self.driver.find_elements_by_class_name(Data.dots)
                    markers=len(dots)-1
                    self.driver.find_element_by_id('download').click()
                    time.sleep(4)
                    p = pwd()
                    self.filename = p.get_download_dir() + "/" + "Schools_per_cluster_report_" + self.month + "_" + self.year + ".csv"
                    print(self.filename)
                    if os.path.isfile(self.filename) != True:
                        return "File Not Downloaded"
                    else:
                        with open(self.filename) as fin:
                            csv_reader = csv.reader(fin, delimiter=',')
                            header = next(csv_reader)
                            teacher = 0
                            for row in csv.reader(fin):
                                teacher += int(row[8])

                            teach = self.driver.find_element_by_id("students").text
                            ta = re.sub('\D', "", teach)

                            if int(teacher) != int(ta):
                                print("Teacher count mismatched", int(teacher), int(ta))
                                count = count + 1
                        os.remove(self.filename)
                    return markers, count

    def check_markers_on_block_map(self):
        cal = GetData()
        count = 0
        self.fname = file_extention()
        self.driver.find_element_by_xpath(Data.hyper_link).click()
        cal.page_loading(self.driver)
        self.driver.find_element_by_id('allBlock').click()
        cal.page_loading(self.driver)
        dots = self.driver.find_elements_by_class_name(Data.dots)
        markers = len(dots) - 1
        self.driver.find_element_by_id(Data.Download).click()
        time.sleep(2)
        p = pwd()
        self.filename = p.get_download_dir() + "/" + "Block_wise_report_" + self.month + "_" + self.year + ".csv"
        if os.path.isfile(self.filename) != True:
            return "File Not Downloaded"
        else:
            with open(self.filename) as fin:
                csv_reader = csv.reader(fin, delimiter=',')
                header = next(csv_reader)
                schools = 0
                teacher =0
                for row in csv.reader(fin):
                    teacher +=int(row[4])
                teach = self.driver.find_element_by_id("students").text
                ta = re.sub('\D', "", teach)
                print("no of missing data",teacher,ta)
                if int(teacher) != int(ta):
                    print("missed teacher count mismatched", int(teacher), int(ta))
                    count = count + 1
            os.remove(self.filename)
        return markers,count

    def check_markers_on_clusters_map(self):
        self.driver.find_element_by_id('allCluster').click()
        cal = GetData()
        count = 0
        self.fname = file_extention()
        cal.page_loading(self.driver)
        dots = self.driver.find_elements_by_class_name(Data.dots)
        markers = len(dots) - 1
        cal.page_loading(self.driver)
        self.driver.find_element_by_id(Data.Download).click()
        time.sleep(3)
        p = pwd()
        self.filename = p.get_download_dir() + "/" + "Cluster_wise_report_" + self.month + "_" + self.year + ".csv"
        if os.path.isfile(self.filename) != True:
            return "File Not Downloaded"
        else:
            with open(self.filename) as fin:
                csv_reader = csv.reader(fin, delimiter=',')
                header = next(csv_reader)
                schools = 0
                teacher = 0
                for row in csv.reader(fin):
                    teacher += int(row[6])
                teach = self.driver.find_element_by_id("students").text
                ta = re.sub('\D', "", teach)
                print("no of missing data",teacher,ta)
                if int(teacher) != int(ta):
                    print("Teacher count mismatched", int(teacher), int(ta))
                    count = count + 1
            os.remove(self.filename)
        return markers, count

    def check_markers_on_school_map(self):
        self.driver.find_element_by_id('allSchool').click()
        cal = GetData()
        count = 0
        self.fname = file_extention()
        cal.page_loading(self.driver)
        result = self.driver.find_elements_by_class_name(Data.dots)
        cal.page_loading(self.driver)
        markers = len(result) - 1
        self.driver.find_element_by_id(Data.Download).click()
        time.sleep(5)
        p = pwd()
        self.filename = p.get_download_dir() + "/" + "School_wise_report_" + self.month + "_" + self.year + ".csv"
        if os.path.isfile(self.filename) != True:
            return "File Not Downloaded"
        else:
            with open(self.filename) as fin:
                csv_reader = csv.reader(fin, delimiter=',')
                header = next(csv_reader)
                teacher = 0
                for row in csv.reader(fin):
                    teacher += int(row[8])
                teach = self.driver.find_element_by_id("students").text
                ta = re.sub('\D', "", teach)
                print("no of missing data",teacher,ta)
                if int(teacher) != int(ta):
                    print("Teacher count mismatched", int(teacher), int(ta))
                    count = count + 1
            os.remove(self.filename)
        return markers, count

    def click_on_hyperlinks(self):
        cal = GetData()
        cal.click_on_state(self.driver)
        cal.page_loading(self.driver)
        dist = Select(self.driver.find_element_by_id("choose_dist"))
        dist.select_by_index(1)
        cal.page_loading(self.driver)
        block = Select(self.driver.find_element_by_id("choose_block"))
        block.select_by_index(1)
        cal.page_loading(self.driver)
        cluster = Select(self.driver.find_element_by_id("choose_cluster"))
        cluster.select_by_index(1)
        cal.page_loading(self.driver)
        self.driver.find_element_by_xpath(Data.hyper_link).click()
        time.sleep(4)
        # self.driver.find_element_by_xpath(Data.sr_school_hyper).click()
        # cal.page_loading(self.driver)
        # self.driver.find_element_by_xpath(Data.sr_cluster_hyper).click()
        # cal.page_loading(self.driver)
        # self.driver.find_element_by_xpath(Data.sr_dist_hyper).click()
        # cal.page_loading(self.driver)
        # result1 = self.driver.find_element_by_id('choose_block').is_displayed()
        # time.sleep(2)
        # result2 = self.driver.find_element_by_id('choose_cluster').is_displayed()
        # time.sleep(2)
        # dist = Select(self.driver.find_element_by_id('choose_dist'))
        # choose_dist = dist.first_selected_option.text
        # return result1, result2, choose_dist

    def check_time_series_overall(self):
        cal = GetData()
        self.p = pwd()
        count = 0
        self.file = file_extention()
        cal.click_on_state(self.driver)
        timeperiods = Select(self.driver.find_element_by_id('period'))
        timeperiods.select_by_visible_text(' Overall ')
        cal.page_loading(self.driver)
        markers = self.driver.find_elements_by_class_name(Data.dots)
        dots = len(markers) - 1
        if markers == 0:
            print('Markers are not present on screen ')
            count = count + 1
        else:
            self.driver.find_element_by_id(Data.Download).click()
            time.sleep(3)
            self.filename = self.p.get_download_dir() + '/' + self.file.exception_district()
            if os.path.isfile(self.filename) != True:
                print("Over all time series csv file is not downloaded")
            else:
                with open(self.filename) as fin:
                    csv_reader = csv.reader(fin, delimiter=',')
                    header = next(csv_reader)
                    schools = 0
                    for row in csv.reader(fin):
                        schools += int(row[3])
                    school = self.driver.find_element_by_id("schools").text
                    sc = re.sub('\D', "", school)
                    if int(sc) != int(schools):
                        print("school count mismatched", int(sc), int(schools))
                        count = count + 1
                os.remove(self.filename)
        return count

    def check_time_series_last_7_days(self):
        cal = GetData()
        self.p = pwd()
        count = 0
        self.file = file_extention()
        cal.click_on_state(self.driver)
        timeperiods = Select(self.driver.find_element_by_id('period'))
        timeperiods.select_by_visible_text(' Last 7 Days ')
        cal.page_loading(self.driver)
        markers = self.driver.find_elements_by_class_name(Data.dots)
        dots = len(markers)-1
        if markers == 0:
            print('Markers are not present on screen ')
            count = count + 1
        else:
            self.driver.find_element_by_id(Data.Download).click()
            time.sleep(3)
            self.filename = self.p.get_download_dir() + '/' + self.file.exception_district()
            if os.path.isfile(self.filename) != True:
                print(" Last 7 Days time series csv file is not downloaded")
            else:
                with open(self.filename) as fin:
                    csv_reader = csv.reader(fin, delimiter=',')
                    header = next(csv_reader)
                    schools = 0
                    for row in csv.reader(fin):
                        schools += int(row[3])
                    school = self.driver.find_element_by_id("schools").text
                    sc = re.sub('\D', "", school)
                    if int(sc) != int(schools):
                        print("school count mismatched", int(sc), int(schools))
                        count = count + 1
                os.remove(self.filename)
        return count

    def check_time_series_last_30_days(self):
        cal = GetData()
        self.p = pwd()
        count = 0
        self.file = file_extention()
        cal.click_on_state(self.driver)
        timeperiods = Select(self.driver.find_element_by_id('period'))
        timeperiods.select_by_visible_text(' Last 30 Days ')
        cal.page_loading(self.driver)
        markers = self.driver.find_elements_by_class_name(Data.dots)
        dots = len(markers) - 1
        if markers == 0:
            print('Markers are not present on screen ')
            count = count + 1
        else:
            cal.page_loading(self.driver)
            self.driver.find_element_by_id(Data.Download).click()
            time.sleep(5)
            self.filename = self.p.get_download_dir() + '/' + self.file.exception_district()
            if os.path.isfile(self.filename) != True:
                print(" Last 30 Days time series csv file is not downloaded")
            else:
                with open(self.filename) as fin:
                    csv_reader = csv.reader(fin, delimiter=',')
                    header = next(csv_reader)
                    schools = 0
                    for row in csv.reader(fin):
                        schools += int(row[3])
                    school = self.driver.find_element_by_id("schools").text
                    sc = re.sub('\D', "", school)
                    if int(sc) != int(schools):
                        print("school count mismatched", int(sc), int(schools))
                        count = count + 1
                os.remove(self.filename)
        return count