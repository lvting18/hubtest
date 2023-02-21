from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from page.BasePage import BasePage
from page.MainPage import MainPage
import time
from selenium.webdriver.common.keys import Keys
import random
import allure
import custom_method.vpmethod as vm


class ImportPage(BasePage):

    # as set default target, every time go to Import page, need collapse C:\
    def iniImport(self):
        vm.log().debug('FUNC: iniImport')
        time.sleep(3)
        c = self.find(By.XPATH, "//Custom[contains(@AutomationId, 'TargetGridControl')]//Text[contains(@Name, 'C:')]")
        ActionChains(self.driver).double_click(c).perform()

    @allure.step('Back to mainpage from Import page')
    def backtomain(self):
        vm.log().debug('FUNC: backtomain')
        self.find(By.XPATH, '//Button[contains(@Name, "Close")]').click()
        self.screen(self.driver, 'AfterClickCloseButton')
        return MainPage()

    @allure.step('Select MTP device')
    def SelectMTP(self, s_folder):
        vm.log().debug('FUNC: SelectMTP')
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'self')]//Text[contains(@Name, '%s')]" % s_folder).click()
        self.driver.implicitly_wait(20)
        return self

    @allure.step('Select one whole folder as source')
    def SelectSourceFolder(self, s_folder):
        vm.log().debug('FUNC: SelectSourceFolder')
        folder_code = 'DMAM.Classes.LocalDirectory'
        s_list = s_folder.split('\\')
        xpath_list = []
        for i in s_list:
            n = s_list.index(i)
            # print(n)
            s_xpath = "//Pane[contains(@AutomationId, 'sc')]" + \
                      "//TreeItem[contains(@Name, '%s')]" % folder_code * (n + 1) + \
                      "//Text[contains(@Name, '%s')]" % i
            # print(s_xpath)
            xpath_list.append(s_xpath)
        vm.log().debug(xpath_list)
        # 返回xpath列表的长度
        l = len(xpath_list)
        vm.log().debug("length of xpath list: "+str(l))
        i = l - 1
        while i >= 0:
            # is_found = self.driver.find_elements_by_xpath(xpath_list[i])
            vm.log().debug("current index of xpath list: "+str(i))
            is_found = self.find(By.XPATH, xpath_list[i])
            if not is_found:
                i = i-1
                vm.log().debug('NOT FOUND')
            else:
                # self.logger().debug('FOUND')
                vm.log().debug('FOUND index: '+str(i))
                for n in range(i, l):
                    p = self.find(By.XPATH, xpath_list[n])
                    ActionChains(self.driver).double_click(p).perform()
                    vm.log().debug('Click index: ' + str(n))
                break
        self.screen(self.driver, 'SelectSourceFolder')
        return self

    @allure.step('Check on [Include subfolder]')
    def ClickIncludeSubFolder(self):
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'self')]//CheckBox[contains(@Name, 'Include subfolders')]").click()
        self.screen(self.driver, 'CheckIncludeSubFolder')

    @allure.step('Select some files as source')
    def SelectFile(self, s_folder):
        vm.log().debug('FUNC: SelectFile')
        self.SelectSourceFolder(s_folder)
        self.find(By.NAME, 'DMAM.Classes.LocalFile').click()
        i = 0
        j = 0
        while i < random.randint(2, 9):
            ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ARROW_DOWN).key_up(Keys.SHIFT).perform()
            i += 1
        while j < random.randint(2, 9):
            ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ARROW_RIGHT).key_up(Keys.SHIFT).perform()
            j += 1
        self.screen(self.driver, 'SelectFile')
        return self

    @allure.step('Get number of selected files')
    def GetSelectedFilesNumber(self):
        vm.log().debug('FUNC: GetSelectedFilesNumber')
        selected = self.driver.find_elements_by_xpath(
            "//Custom[contains(@AutomationId, 'ImportDetailPage')]//Button[contains(@AutomationId, 'PageheaderButton')]")[1].text
        vm.log().debug(selected)
        file_number = selected.split()[0]
        vm.log().debug(file_number)
        return int(file_number)

    @allure.step('Select target folder')
    def SelectTargetFolder(self, t_folder):
        vm.log().debug('FUNC: SelectTargetFolder')
        t_list = t_folder.split('\\')
        # for i in t_list:
        #     p = self.find(By.XPATH,
        #                   "//Custom[contains(@AutomationId, 'TargetGridControl')]//Text[contains(@Name, '%s')]" % i)
        #     ActionChains(self.driver).double_click(p).perform()
        xpath_list = []
        for i in t_list:
            t_xpath = "//Custom[contains(@AutomationId, 'TargetGridControl')]//Text[contains(@Name, '%s')]" % i
            # print(s_xpath)
            xpath_list.append(t_xpath)
        vm.log().debug(xpath_list)
        # 返回xpath列表的长度
        l = len(xpath_list)
        vm.log().debug(l)
        i = l - 1
        vm.log().debug(i)
        while i >= 0:
            # is_found = self.driver.find_elements_by_xpath(xpath_list[i])
            is_found = self.find(By.XPATH, xpath_list[i])
            if not is_found:
                i = i - 1
                vm.log().debug('NOT FOUND')
            else:
                # self.logger().debug('FOUND')
                vm.log().debug('FOUND')
                for n in range(i, l):
                    p = self.find(By.XPATH, xpath_list[n])
                    ActionChains(self.driver).double_click(p).perform()
                break
        self.screen(self.driver, 'SelectTargetFolder')

    @allure.step(r"New target folder")
    def NewTargetFolder(self, t_folder='F:', target_name='default'):
        vm.log().debug('FUNC: NewTargetFolder')
        t_list = t_folder.split('\\')
        # print(t_list)
        xpath_list = []
        for i in t_list:
            t_xpath = "//Custom[contains(@AutomationId, 'TargetGridControl')]//Text[contains(@Name, '%s')]" % i
            # print(s_xpath)
            xpath_list.append(t_xpath)
        vm.log().debug(xpath_list)
        # 返回xpath列表的长度
        l = len(xpath_list)
        vm.log().debug(l)
        i = l - 1
        vm.log().debug(i)
        while i >= 0:
            # is_found = self.driver.find_elements_by_xpath(xpath_list[i])
            is_found = self.find(By.XPATH, xpath_list[i])
            if not is_found:
                i = i - 1
                vm.log().debug('NOT FOUND')
            else:
                # self.logger().debug('FOUND')
                vm.log().debug('FOUND')
                for n in range(i, l):
                    p = self.find(By.XPATH, xpath_list[n])
                    ActionChains(self.driver).double_click(p).perform()
                break
        ActionChains(self.driver).send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()
        if target_name == 'default':
            target_name = time.strftime('target_%Y%m%d_%H%M%S', time.localtime(time.time()))
        self.driver.find_element_by_accessibility_id("EnterName").send_keys(target_name)
        self.driver.find_element_by_accessibility_id('okbutton').click()
        t_list.append(target_name)
        target_path = "\\".join(t_list)
        self.screen(self.driver, 'NewTargetFolder')
        return target_path

    @allure.step('Click Import button')
    def ClickImport(self):
        vm.log().debug('FUNC: ClickImport')
        self.driver.find_element_by_accessibility_id('importbutton').click()
        self.screen(self.driver, 'ClickImport')

    @allure.step('Uncheck import target folder; Click Add selection button')
    def ClickAddToLibrary(self):
        vm.log().debug('FUNC: ClickAddToLibrary')
        self.driver.find_element_by_accessibility_id('AddFile').click()
        self.driver.find_element_by_accessibility_id('AddButton').click()
        self.screen(self.driver, 'ClickAddToLibrary')

    @allure.step('Judge if it is importing')
    def IsImportDialogOpen(self):
        vm.log().debug('FUNC: IsImportDialogOpen')
        i = (By.XPATH, "//Custom[contains(@AutomationId, 'ImportFilesProgressPage')]")
        try:
            WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(i))
            return True
        except:
            return False

    @allure.step('Waiting for importing finished')
    def WaitingImportFinish(self):
        vm.log().debug('FUNC: WaitingImportFinish')
        # wait until import finished dialog pop up
        for i in range(600):
            try:
                WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located((
                    By.XPATH, "//Custom[contains(@AutomationId, 'ImportFilesResponsePage')]"
                              "//Button[contains(@AutomationId, 'GoToButton')]")))
                vm.log().debug('Import successfully')
                break
            except:
                vm.log().debug('Not find Go to library')
                try:
                    WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located((By.NAME, 'Retry')))
                    vm.log().debug('Import failed')
                    break
                except:
                    vm.log().debug('Not find Gotolibrary and Retry')
                    continue

    def WaitingAddFinish(self):
        vm.log().debug('FUNC: WaitingImportFinish')
        # wait until add finished dialog pop up
        for i in range(600):
            try:
                WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located((
                    By.XPATH, "//Custom[contains(@AutomationId, 'ImportAddFilesResponsePage')]"
                              "//Button[contains(@AutomationId, 'GoToButton')]")))
                vm.log().debug('Import successfully')
                break
            except:
                vm.log().debug('Not find Go to library')
                try:
                    WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located((By.NAME, 'Retry')))
                    vm.log().debug('Import failed')
                    break
                except:
                    vm.log().debug('Not find Gotolibrary and Retry')
                    continue

    @allure.step('Close Import dialog, stay at Import page')
    def CloseImportDialog(self):
        vm.log().debug('FUNC: CloseImportDialog')
        self.screen(self.driver, 'AfterImportFinished')
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'ImportFilesResponsePage')]"
                            "//Button[contains(@AutomationId, 'OKButton')]").click()
        self.screen(self.driver, 'AfterCloseImportDialog')

    @allure.step('Close Add to library dialog, stay at Import page')
    def CloseAddDialog(self):
        vm.log().debug('FUNC: CloseAddDialog')
        self.screen(self.driver, 'AfterImportFinished')
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'ImportAddFilesResponsePage')]"
                            "//Button[contains(@AutomationId, 'OKButton')]").click()
        self.screen(self.driver, 'AfterCloseaddDialog')

    @allure.step('Click Go to library button of Import dialog')
    def GoToLibrary(self):
        vm.log().debug('FUNC: GoToLibrary')
        self.screen(self.driver, 'AfterImportFinished')
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'ImportFilesResponsePage')]"
                            "//Button[contains(@AutomationId, 'GoToButton')]").click()
        self.screen(self.driver, 'ClickGoToLibrary')

    @allure.step('Change view')
    def ChangeView(self, view='all'):
        vm.log().debug('FUNC: ChangeView')
        self.screen(self.driver, 'BeforeChangeView')
        all_views = ['ViewbyList', 'ViewbySmall', 'ViewbyMedium', 'ViewbyLarge']
        random.shuffle(all_views)
        if view == 'random':
            v = [all_views.pop()]
            all_views = v
        for viewby in all_views:
            self.find(By.XPATH, "//Custom[contains(@AutomationId, 'ImportDetailPage')]"
                                "//Button[contains(@AutomationId, 'ViewbyButton')]").click()
            self.driver.find_element_by_accessibility_id(viewby).click()
        self.screen(self.driver, 'AfterChangeView')

    @allure.step('Change group')
    def ChangeGroup(self, group='all'):
        vm.log().debug('FUNC: ChangeGroup')
        self.screen(self.driver, 'BeforeChangeGroup')
        all_groups = ['GroupbyNone', 'GroupbyDate', 'GroupbyType']
        random.shuffle(all_groups)
        if group == 'random':
            g = [all_groups.pop()]
            all_groups = g
        for groupby in all_groups:
            self.find(By.XPATH, "//Custom[contains(@AutomationId, 'ImportDetailPage')]"
                                "//Button[contains(@AutomationId, 'GroupbyButton')]").click()
            self.driver.find_element_by_accessibility_id(groupby).click()
        self.screen(self.driver, 'AfterChangeGroup')

    @allure.step('Change sort')
    def ChangeSort(self, sort='all'):
        vm.log().debug('FUNC: ChangeSort')
        self.screen(self.driver, 'BeforeChangeSort')
        all_sorts = ['SortbyName', 'SortbyDate', 'SortbyFolder', 'SortbyType', 'SortbySize']
        random.shuffle(all_sorts)
        if sort == 'random':
            random.shuffle(all_sorts)
            s = [all_sorts.pop()]
            all_sorts = s
        for sortby in all_sorts:
            self.find(By.XPATH, "//Custom[contains(@AutomationId, 'ImportDetailPage')]"
                                "//Button[contains(@AutomationId, 'SortbyButton')]").click()
            self.driver.find_element_by_accessibility_id(sortby).click()
        self.screen(self.driver, 'AfterChangeSort')

