import random
import sys
import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from page.BasePage import BasePage
import time
import custom_method.vpmethod as vm
import custom_method.CompareImages as cs


class MainPage(BasePage):
    t = ''

    @allure.step('Go to Import page')
    def gotoImport(self):
        vm.log().debug('FUNC: gotoImport')
        from page.ImportPage import ImportPage
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'importb')]").click()
        return ImportPage()

    @allure.step('Go to Settings page')
    def gotoSettings(self):
        vm.log().debug('FUNC: gotoSettings')
        from page.SettingsPage import SettingsPage
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'setting')]").click()
        return SettingsPage()

    # select random item
    def selectItem(self, s_type, s_path='random'):
        vm.log().debug('FUNC: selectItem')
        folder_code = ''
        xpath_list = []
        # 从数据库随机取一个id以及它的父节点，以列表的形式返回
        path_list = vm.db_random(s_type)
        # self.logger().debug(path_list)
        # vm.log().debug(path_list)
        # 从列表的最后两位取id和对应的表名
        info = path_list[-2:]
        path_list = path_list[:-2]
        # 如果调用的函数的时候，传入了path，通过字符串分割法，生成列表
        if s_path is not 'random':
            path_list = s_path.split('\\')
        # 此时列表里是文件目录的名称[a,b,c], a是All下面的第一层，c是子
        # 针对library和collection，合成相应的xpath，[a_xpath, b_xpath, c_xpath]
        if s_type == 'library':
            folder_code = 'DMAM.Classes.DataDirectory'
        elif s_type == 'collection' or s_type == 'collection_set' or s_type == 'collection&set':
            folder_code = 'DMAM.Classes.CollectionDirectory'
        n = 0
        for p in path_list:
            t_xpath = "//TreeItem[contains(@Name, '%s')]" % folder_code * (n + 2)
            s_xpath = t_xpath + "//Text[@Name='%s']" % p
            # s_xpath = t_xpath + "//Text[contains(@Name, '%s')]" % p
            xpath_list.append(s_xpath)
            n = n+1
        # self.logger().debug(xpath_list)
        vm.log().debug(xpath_list)
        # 返回xpath列表的长度
        l = len(xpath_list)
        i = l-1
        # 从最后的一个文件夹开始找，如果没找到，继续找上一级的文件夹
        while i >= 0:
            # is_found = self.driver.find_elements_by_xpath(xpath_list[i])
            is_found = self.find(By.XPATH, xpath_list[i])
            if not is_found:
                i = i-1
                vm.log().debug('Find item to double click: NOT FOUND')
            else:
                vm.log().debug('Find item to double click: FOUND')
                for n in range(i, l):
                    MainPage.t = self.find(By.XPATH, xpath_list[n])
                    ActionChains(self.driver).double_click(MainPage.t).perform()
                break
        return info

    @allure.step('Select folder')
    def selectFolder(self, s_path='random'):
        vm.log().debug('FUNC: selectFolder')
        folder_id = self.selectItem('library', s_path)[-1]
        vm.log().debug('Selected folder id: %s' % folder_id)
        self.screen(self.driver, 'SelectFolder')
        return folder_id

    @allure.step('Select one item from collection or collection set')
    def selectFromCollections(self):
        # return a list, [selected_db_table, selected_item_id]
        vm.log().debug('FUNC: selectFromCollections')
        info = self.selectItem('collection&set')
        self.screen(self.driver, 'SelectAnyCollectionOrSet')
        return info

    @allure.step('Select collection')
    def selectCollection(self):
        vm.log().debug('FUNC: selectCollection')
        collection_id = self.selectItem('collection')[-1]
        vm.log().debug('Selected collection id: ')
        vm.log().debug(collection_id)
        self.screen(self.driver, 'SelectCollection')
        return collection_id

    @allure.step('Select collection set')
    def selectCollectionSet(self):
        vm.log().debug('FUNC: selectCollectionSet')
        collection_set_id = self.selectItem('collection_set')[-1]
        vm.log().debug('Selected collection set id: ')
        vm.log().debug(collection_set_id)
        self.screen(self.driver, 'SelectCollectionSet')
        return collection_set_id

    def selectFile(self, s_type, n='all', s_path='random'):
        vm.log().debug('FUNC: selectFile')
        f_xpath = ''
        item_id = ''
        if s_type == 'library_file':
            item_id = self.selectFolder(s_path)
            f_xpath = "//ListItem[contains(@Name, 'DMAM.Classes.DataFile')]"
            while True:
                if not self.driver.find_elements_by_xpath(f_xpath):
                    item_id = self.selectFolder(s_path)
                else:
                    break
        elif s_type == 'collection_file':
            item_id = self.selectFromCollections()[-1]
            f_xpath = "//ListItem[contains(@Name, 'DMAM.Classes.CollectionFile')]"
            while True:
                if not self.driver.find_elements_by_xpath(f_xpath):
                    item_id = self.selectFromCollections()[-1]
                else:
                    break
        if n == 'all':
            vm.log().debug('Select all files')
            self.find(By.XPATH, "//Button[contains(@AutomationId, 'PageheaderButton')]").click()
        elif n == 'random':
            vm.log().debug('Select random files')
            # click first file
            self.find(By.XPATH, f_xpath).click()
            # move down random times, <10
            i = 0
            j = 0
            while i < random.randint(1, 10):
                ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ARROW_DOWN).key_up(Keys.SHIFT).perform()
                i += 1
            while j < random.randint(1, 10):
                ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ARROW_RIGHT).key_up(Keys.SHIFT).perform()
                j += 1
        elif n == '1':
            vm.log().debug('Select random files')
            # click first file
            self.find(By.XPATH, f_xpath).click()
            # move down random times, <10
            i = 0
            j = 0
            while i < random.randint(1, 10):
                ActionChains(self.driver).key_down(Keys.ARROW_DOWN).perform()
                i += 1
            while j < random.randint(1, 10):
                ActionChains(self.driver).key_down(Keys.ARROW_RIGHT).perform()
                j += 1
        MainPage.t = self.find(By.XPATH, "//ListItem[contains(@ClassName, 'ListBoxItem')]")
        return item_id

    @allure.step('Select folder file')
    def selectFolderFile(self, n='1', s_path='random'):
        vm.log().debug('FUNC: selectFolderFile')
        folder_id = self.selectFile('library_file', n, s_path)
        vm.log().debug('Selected folder: %s' % folder_id)
        self.screen(self.driver, 'SelectCustomedFolderFiles')
        return folder_id

    @allure.step('Select random collection file')
    def selectRandomCollectionFile(self):
        vm.log().debug('FUNC: selectRandomCollectionFile')
        collection_id = self.selectFile('collection_file', 'random')
        vm.log().debug('Selected collection: %s' % collection_id)
        self.screen(self.driver, 'SelectOneRandomCollectionFile')
        return collection_id

    @allure.step('Select all collection file')
    def selectAllCollectionFile(self):
        vm.log().debug('FUNC: selectAllCollectionFile')
        collection_id = self.selectFile('collection_file', 'all')
        self.screen(self.driver, 'SelectAllCollectionFiles')
        return collection_id

    @allure.step('Click page head')
    def clickPageHead(self):
        vm.log().debug('FUNC: clickPageHead')
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'PageheaderButton')]").click()
        self.screen(self.driver, 'ClickPageHead')
        return self

    @allure.step('Select all files by ctrl+A')
    def selectAll(self):
        vm.log().debug('FUNC: selectAll')
        ActionChains(self.driver).key_down(Keys.CONTROL).key_down('a').key_up(Keys.CONTROL).perform()
        self.screen(self.driver, 'ctrlA')

    @allure.step('Get selected files number')
    def getSelectedFileNumber(self):
        vm.log().debug('FUNC: GetSelectedFilesNumber')
        selected = self.driver.find_elements_by_xpath(
            "//Button[contains(@AutomationId, 'PageheaderButton')]")[1].text
        self.screen(self.driver, 'getSelectedFileNumber')
        vm.log().debug(selected)
        file_number = selected.split()[0]
        vm.log().debug(file_number)
        return int(file_number)

    @allure.step('Right click')
    def rightClick(self):
        vm.log().debug('FUNC: rightClick')
        ActionChains(self.driver).context_click(MainPage.t).perform()
        self.screen(self.driver, 'rightClick')
        return self

    # @allure.step('Open menu in page head')
    # def topMenu(self):
    #     vm.log().debug('FUNC: topMenu')
    #     WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
    #         (By.XPATH, "//Button[contains(@AutomationId, 'CollectionButton')]")))
    #     self.find(By.XPATH, "//Button[contains(@AutomationId, 'CollectionButton')]").click()

    @allure.step('Open folder menu by tab key')
    def folderMenu(self):
        vm.log().debug('FUNC: folderMenu')
        ActionChains(self.driver).key_down(Keys.TAB).key_down(Keys.ENTER).perform()
        self.screen(self.driver, 'folderMenu')

    # remove file menu in Build#442
    # @allure.step('Open file menu by tab key')
    # def fileMenu(self):
    #     vm.log().debug('FUNC: fileMenu')
    #     ActionChains(self.driver).key_down(Keys.TAB).key_down(Keys.TAB).key_down(Keys.TAB).key_down(Keys.ENTER).perform()

    @allure.step('Add customed root folder')
    def addRootFolder(self, folder_path):
        vm.log().debug('FUNC: addRootFolder')
        library_all = self.find(By.XPATH, "//TreeItem[contains(@Name, 'DMAM.Classes.DataDirectory')]"
                                          "//Text[contains(@Name, 'All')]")
        ActionChains(self.driver).context_click(library_all).perform()
        self.find(By.NAME, 'Add root folder').click()
        self.screen(self.driver, 'OpenAddRootFolderDialog')
        time.sleep(1)
        # self.find(By.XPATH, "//Window[contains(@Name, 'Select Folder')]//Edit[contains(@Name, 'Folder:')]").click()
        self.find(By.XPATH, "//Window[contains(@Name, 'Select Folder')]//Edit[contains(@Name, 'Folder:')]").send_keys(folder_path)
        self.screen(self.driver, 'InputFolderPath')
        self.find(By.XPATH, "//Window[contains(@Name, 'Select Folder')]//Button[contains(@Name, 'Select Folder')]").click()

    @allure.step('Find Add to target collection in the menu')
    def findAddToTarget(self):
        # vm.log().debug('FUNC: findAddToTarget')
        # result = self.find(By.NAME, 'Add to target collection')
        # vm.log().debug(result)
        # return result
        addToTarget = (By.NAME, "Add to target collection")
        try:
            WebDriverWait(self.driver, 2).until(EC.visibility_of_any_elements_located(addToTarget))
            return True
        except:
            return False

    @allure.step('Click Remove from target collection in the menu')
    def clickRemoveFromTarget(self):
        vm.log().debug('FUNC: clickRemoveFromTarget')
        self.find(By.NAME, 'Remove from target collection').click()
        self.screen(self.driver, 'AfterClickRemoveFromTargetCollection')
        self.WaitProgressDialogClosed()
        self.screen(self.driver, 'AfterCompleteRemovingFromTargetCollection')
        return self

    @allure.step('Click Add to target collection in the menu')
    def clickAddToTarget(self):
        vm.log().debug('FUNC: clickAddToTarget')
        self.find(By.NAME, 'Add to target collection').click()
        self.screen(self.driver, 'AfterClickAddToTargetCollectionByFileMenu')
        self.WaitProgressDialogClosed()
        self.screen(self.driver, 'AfterCompleteAddingToTargetCollection')
        return self

    @allure.step('add to target collection by tab to crosshair and press ENTER key')
    def addToTargetCollectionByCrosshair(self):
        vm.log().debug('FUNC: addToTargetCollectionByCrosshair')
        ActionChains(self.driver).key_down(Keys.TAB).key_down(Keys.ENTER).perform()
        self.screen(self.driver, 'AfterAddToTargetCollectionByCrosshair')

    @allure.step('Select collection as target collection after open set target collection dialog')
    def setTargetCollection(self):
        vm.log().debug('FUNC: setTargetCollection')
        self.screen(self.driver, 'BeforeSelectSetAndCollection')
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'SetTargetDialog')]"
                            "//ComboBox[contains(@AutomationId, 'SetCombobox')]").click()
        ActionChains(self.driver).key_down(Keys.ARROW_DOWN).key_down(Keys.ARROW_DOWN).key_down(Keys.ENTER).perform()
        self.screen(self.driver, 'AfterSelectSet')
        self.find(By.XPATH, "//ComboBox[contains(@AutomationId, 'CollectionCombobox')]").click()
        ActionChains(self.driver).key_down(Keys.ARROW_DOWN).key_down(Keys.ARROW_DOWN).key_down(Keys.ENTER).perform()
        self.screen(self.driver, 'AfterSelectCollection')
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'okbutton')]").click()
        WebDriverWait(self.driver, 60).until(EC.invisibility_of_element_located(
            (By.XPATH, "//Custom[contains(@AutomationId, 'SetTargetDialog')]")))
        self.screen(self.driver, 'AfterSetTargetCollection')

    @allure.step('Close set target collection dialog')
    def closeSetTargetCollectionDialog(self):
        vm.log().debug('FUNC: closeSetTargetCollectionDialog')
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'SetTargetDialog')]"
                            "//Button[contains(@AutomationId, 'cancelbutton')]").click()
        self.screen(self.driver, 'AfterCancelSetTargetCollection')

    @allure.step('Click Create sub folder option in the menu')
    def openCreateFolderDailog(self):
        vm.log().debug('FUNC: openCreateFolderDailog')
        self.find(By.XPATH, "//MenuItem[contains(@Name, 'Create sub folder inside')]").click()
        self.screen(self.driver, 'openCreateFolderDailog')

    @allure.step('Input folder name, confirm create')
    def confirmCreateFolder(self, s='default'):
        vm.log().debug('FUNC: confirmCreateFolder')
        if s == 'default':
            s = time.strftime('subfolder_%Y%m%d_%H%M%S', time.localtime(time.time()))
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'CreateImportFolderDialog')]"
                            "//Edit[contains(@AutomationId, 'EnterName')]")
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'CreateImportFolderDialog')]"
                            "//Edit[contains(@AutomationId, 'EnterName')]").send_keys(s)
        self.screen(self.driver, 'InputFolderName')
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'CreateImportFolderDialog')]"
                            "//Button[contains(@AutomationId, 'okbutton')]").click()
        return s

    def waitCreateFolderComplete(self):
        WebDriverWait(self.driver, 60).until(EC.invisibility_of_element_located(
            (By.XPATH, "//Custom[contains(@AutomationId, 'CreateImportFolderDialog')]")))
        return self

    def getCreateFolderErr(self):
        vm.log().debug('FUNC: getCreateFolderErr')
        # find two elements, select second element, get the error message
        error_message = self.driver.find_elements_by_xpath(
                "//Custom[contains(@AutomationId, 'CreateImportFolderDialog')]//Text[contains(@ClassName, 'TextBlock')]")[1].text
        self.screen(self.driver, 'CreateFolderErr')
        return error_message

    @allure.step('Close create folder dialog')
    def closeCreateFolderDialog(self):
        vm.log().debug('FUNC: closeCreateFolderDialog')
        # self.find(By.XPATH, "//Custom[contains(@AutomationId, 'CreateImportFolderDialog')]"
        #                     "//Button[contains(@AutomationId, 'cancelbutton')]").click()
        ActionChains(self.driver).key_down(Keys.ESCAPE).perform()

    @allure.step('Click Rename option in the menu')
    def openRenameDialog(self):
        vm.log().debug('FUNC: openRenameDialog')
        self.find(By.XPATH, "//MenuItem[contains(@Name, 'Rename')]").click()
        self.screen(self.driver, 'openRenameDialog')

    @allure.step('Click Rename collection set in the menu')
    def openRenameCollectionSetDialog(self):
        vm.log().debug('FUNC: openRenameCollectionSetDialog')
        self.find(By.XPATH, "//MenuItem[contains(@Name, 'Rename collection set')]").click()
        self.screen(self.driver, 'openRenameCollectionSetDialog')

    @allure.step('Input new name and confirm')
    def confirmRename(self, s='default'):
        vm.log().debug('FUNC: confirmRename')
        if s == 'default':
            s = time.strftime('rename_%Y%m%d_%H%M%S', time.localtime(time.time()))
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'RenameDialog')]"
                            "//Edit[contains(@AutomationId, 'EnterName')]")
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'RenameDialog')]"
                            "//Edit[contains(@AutomationId, 'EnterName')]").send_keys(s)
        self.screen(self.driver, 'InputNewName')
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'RenameDialog')]"
                            "//Button[contains(@AutomationId, 'okbutton')]").click()
        return s

    def waitRenameComplete(self):
        WebDriverWait(self.driver, 60).until(EC.invisibility_of_element_located(
            (By.XPATH, "//Custom[contains(@AutomationId, 'RenameDialog')]")))
        return self

    def getRenameErr(self):
        vm.log().debug('FUNC: getRenameErr')
        error_message = self.driver.find_elements_by_xpath(
            "//Custom[contains(@AutomationId, 'RenameDialog')]//Text[contains(@AutomationId, 'errortext')]")[0].text
        self.screen(self.driver, 'RenameErr')
        return error_message

    @allure.step('Close rename dialog by click Cancel button')
    def closeRenameDialog(self):
        vm.log().debug('FUNC: closeRenameDialog')
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'RenameDialog')]"
                            "//Button[contains(@AutomationId, 'cancelbutton')]").click()

    @allure.step('Click Delete option in the menu ')
    def openDeleteFolderDialog(self):
        vm.log().debug('FUNC: openDeleteFolderDialog')
        self.find(By.XPATH, "//MenuItem[contains(@Name, 'Delete')]").click()
        self.screen(self.driver, 'openDeleteFolderDialog')

    @allure.step('Check on delete from PC checkbox')
    def checkOnDeleteFromPC(self):
        vm.log().debug('FUNC: checkOnDeleteFromPC')
        self.find(By.XPATH, "//CheckBox[contains(@AutomationId, 'DeleteHD')]").click()
        self.screen(self.driver, 'checkOnDeleteFromPC')

    @allure.step('Click OK button')
    def confirmDeleteFolder(self):
        vm.log().debug('FUNC: confirmDeleteFolder')
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'DeleteFolderDialog')]"
                            "//Button[contains(@AutomationId, 'okbutton')]").click()
        return self

    def waitDeleteFolderFromDbCompleted(self):
        vm.log().debug('FUNC: waitDeleteFromPcCompleted')
        WebDriverWait(self.driver, 60).until(EC.invisibility_of_element_located(
            (By.XPATH, "//Custom[contains(@AutomationId, 'DeleteFolderDialog')]")))
        self.screen(self.driver, 'CompleteDeletFolderFromDb')

    def waitDeleteFromPcCompleted(self):
        vm.log().debug('FUNC: waitDeleteFromPcCompleted')
        WebDriverWait(self.driver, 60).until(EC.invisibility_of_element_located(
            (By.XPATH, "//Custom[contains(@AutomationId, 'DeleteFolderProgressPage')]")))
        self.screen(self.driver, 'CompleteDeleteFromPc')

    def waitDeleteFileFromDbCompleted(self):
        vm.log().debug('FUNC: waitDeleteFromPcCompleted')
        WebDriverWait(self.driver, 60).until(EC.invisibility_of_element_located(
            (By.XPATH, "//Custom[contains(@AutomationId, 'DeleteDialog')]")))
        self.screen(self.driver, 'CompleteDeleteFileFromDb')

    @allure.step('Close delete folder dialog')
    def closeDeleteFolderDialog(self):
        vm.log().debug('FUNC: closeDeleteFolderDialog')
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'DeleteFolderDialog')]"
                            "//Button[contains(@AutomationId, 'cancelbutton')]").click()
        self.screen(self.driver, 'AfterCancelDeleteFolder')

    @allure.step('Click OK button')
    def ConfirmDeleteFiles(self):
        vm.log().debug('FUNC: ConfirmDeleteFiles')
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'DeleteDialog')]"
                            "//Button[contains(@AutomationId, 'okbutton')]").click()

    @allure.step('Click [Create collection]')
    def openCreateCollectionDialog(self):
        vm.log().debug('FUNC: openCreateCollectionDialog')
        self.find(By.XPATH, "//MenuItem[contains(@Name, 'Create collection')]").click()
        self.screen(self.driver, 'openCreateCollectionDialog')
        return self

    @allure.step('Check on [Set as target collection]')
    def checkOnSetAsTarget(self):
        vm.log().debug('FUNC: checkOnSetAsTarget')
        self.find(By.XPATH, "//CheckBox[contains(@AutomationId, 'TargetCollection')]").click()
        self.screen(self.driver, 'checkOnSetAsTarget')
        return self

    @allure.step('Input name, ok')
    def confirmCreateCollection(self, s='default'):
        vm.log().debug('FUNC: confirmCreateCollection')
        if s == 'default':
            s = time.strftime('collection_%Y%m%d_%H%M%S', time.localtime(time.time()))
        self.find(By.XPATH, "//Edit[contains(@AutomationId, 'EnterName')]").send_keys(s)
        self.screen(self.driver, 'InputCollectionName')
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'okbutton')]").click()
        self.screen(self.driver, 'AfterCreateCollection')
        return s

    @allure.step('Input name, select collection, ok')
    def createCollectionForFiles(self):
        vm.log().debug('FUNC: createCollectionForFiles')
        s = time.strftime('collection_%Y%m%d_%H%M%S', time.localtime(time.time()))
        self.find(By.XPATH, "//Edit[contains(@AutomationId, 'EnterName')]").send_keys(s)
        self.find(By.XPATH, "//ComboBox[contains(@AutomationId, 'SetCombobox')]").click()
        ActionChains(self.driver).key_down(Keys.ARROW_DOWN).key_down(Keys.ENTER).perform()
        self.screen(self.driver, 'InputNameAndSelectCollectionSet')
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'okbutton')]").click()
        self.WaitProgressDialogClosed()
        return s

    @allure.step('Get error when create collection')
    def createCollectionError(self):
        vm.log().debug('FUNC: createCollectionError')
        error_message = self.driver.find_elements_by_xpath(
            "//Custom[contains(@AutomationId, 'CreateCollectionDialog')]//Text[contains(@ClassName, 'TextBlock')]")[2].text
        self.screen(self.driver, 'createCollectionError')
        return error_message

    @allure.step('Close create collection dialog')
    def closeCreateCollectionDialog(self):
        vm.log().debug('FUNC: closeCreateCollectionDialog')
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'cancelbutton')]").click()
        self.screen(self.driver, 'CancelCreateCollection')

    @allure.step('Click [Create collection set]')
    def openCreateCollectionSet(self):
        vm.log().debug('FUNC: openCreateCollectionSet')
        self.find(By.XPATH, "//MenuItem[contains(@Name, 'Create collection set')]").click()
        self.screen(self.driver, 'openCreateCollectionSet')

    @allure.step('Input name, ok')
    def confirmCreateCollectionSet(self, s='default'):
        vm.log().debug('FUNC: confirmCreateCollectionSet')
        if s == 'default':
            s = time.strftime('collection_set_%Y%m%d_%H%M%S', time.localtime(time.time()))
        self.find(By.XPATH, "//Edit[contains(@AutomationId, 'EnterName')]").send_keys(s)
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'okbutton')]").click()
        self.screen(self.driver, 'AfterCreateCollectionSet')
        return s

    @allure.step('Get error when create collection set')
    def createCollectionSetError(self):
        vm.log().debug('FUNC: createCollectionSetError')
        error_message = self.driver.find_elements_by_xpath(
            "//Custom[contains(@AutomationId, 'CreateCollectionSetDialog')]//Text[contains(@ClassName, 'TextBlock')]")[
            1].text
        self.screen(self.driver, 'createCollectionSetError')
        return error_message

    @allure.step('Close create collection set dialog')
    def closeCreateCollectionSetDialog(self):
        vm.log().debug('FUNC: closeCreateCollectionSetDialog')
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'cancelbutton')]").click()
        self.screen(self.driver, 'CancelCreateCollectionSet')

    @allure.step('Click [Set as target collection]')
    def setAsTargetCollection(self):
        vm.log().debug('FUNC: setAsTargetCollection')
        self.find(By.XPATH, "//MenuItem[contains(@Name, 'Set as target collection')]").click()
        self.screen(self.driver, 'AfterSetTargetCollection')

    @allure.step('Click [Move collection], select collection set, ok')
    def moveCollection(self):
        vm.log().debug('FUNC: moveCollection')
        self.find(By.XPATH, "//MenuItem[@Name='Move collection']").click()
        self.find(By.XPATH, "//ComboBox[contains(@AutomationId, 'SetCombobox')]").click()
        ActionChains(self.driver).key_down(Keys.ARROW_DOWN).key_down(Keys.ARROW_DOWN).key_down(Keys.ENTER).perform()
        self.screen(self.driver, 'AfterSelectTargetCollectionSet')
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'okbutton')]").click()
        self.screen(self.driver, 'AfterMoveCollectionToTargetSet')
        # 因为往下移了2位，在数据库里找到第二个collection set，就是目标set
        target_id = vm.db_random('collection_set', '2')[-1]
        return target_id

    @allure.step('Click [Move collection set], select collection set, ok')
    def moveCollectionSet(self, moved):
        vm.log().debug('FUNC: moveCollectionSet')
        self.find(By.XPATH, "//MenuItem[contains(@Name, 'Move collection set')]").click()
        self.find(By.XPATH, "//ComboBox[contains(@AutomationId, 'SetCombobox')]").click()
        ActionChains(self.driver).key_down(Keys.ARROW_DOWN).key_down(Keys.ENTER).perform()
        self.screen(self.driver, 'AfterSelectTargetCollectionSet')
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'okbutton')]").click()
        self.screen(self.driver, 'AfterMoveCollectionSetToTargetSet')
        target_set_id = vm.db_selected_set_when_move_collection_set(moved)
        return target_set_id

    @allure.step('Click [Remove *], ok')
    def removeCollection(self):
        vm.log().debug('FUNC: removeCollection')
        self.find(By.XPATH, "//MenuItem[contains(@Name, 'Remove collection')]").click()
        self.screen(self.driver, 'BeforeRemoveCollection')
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'okbutton')]").click()

    @allure.step('Click [Remove collection set], ok')
    def removeCollectionSet(self):
        vm.log().debug('FUNC: removeCollectionSet')
        self.find(By.XPATH, "//MenuItem[contains(@Name, 'Remove collection set')]").click()
        self.screen(self.driver, 'BeforeRemoveCollectionSet')
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'okbutton')]").click()

    @allure.step('Click [Remove collection set], ok')
    def removeCollectionFile(self):
        vm.log().debug('FUNC: removeCollectionFile')
        self.find(By.XPATH, "//MenuItem[@Name='Remove']").click()
        self.screen(self.driver, 'BeforeRemoveCollectionFile')
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'okbutton')]").click()
        d = (By.XPATH, "//Button[contains(@AutomationId, 'Detailsbutton')]")
        WebDriverWait(self.driver, 600).until(EC.element_to_be_clickable(d))

    @allure.step('Click [Add to collection], select collection set, select collection, ok')
    def addToCollection(self):
        vm.log().debug('FUNC: addToCollection')
        result = vm.db_check_collection()
        vm.log().debug(result)
        self.find(By.XPATH, "//MenuItem[@Name='Add to collection']").click()
        self.screen(self.driver, 'OpenAddToCollectionDialog')
        self.find(By.XPATH, "//ComboBox[contains(@AutomationId, 'SetCombobox')]").click()
        ActionChains(self.driver).key_down(Keys.ARROW_DOWN).key_down(Keys.ENTER).perform()
        self.find(By.XPATH, "//ComboBox[contains(@AutomationId, 'CollectionCombobox')]").click()
        ActionChains(self.driver).key_down(Keys.ARROW_DOWN).key_down(Keys.ENTER).perform()
        self.screen(self.driver, 'AfterSelectSetAndCollection')
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'okbutton')]").click()
        WebDriverWait(self.driver, 60).until(EC.invisibility_of_element_located(
            (By.XPATH, "//Custom[contains(@AutomationId, 'AddToCollectionDialog')]")))
        self.screen(self.driver, 'AfterAddToSelectedCollection')
        # todo: improve function db_selected_collection
        selected_collection_id = vm.db_selected_collection(result)
        return selected_collection_id

    @allure.step('Click [Move to collection], select collection set, select collection, ok')
    def moveCollectionFile(self):
        vm.log().debug('FUNC: moveCollectionFile')
        result = vm.db_check_collection()
        self.find(By.XPATH, "//MenuItem[contains(@Name, 'Move to collection')]").click()
        self.screen(self.driver, 'OpenMoveCollectionFileDialog')
        self.find(By.XPATH, "//ComboBox[contains(@AutomationId, 'SetCombobox')]").click()
        ActionChains(self.driver).key_down(Keys.ARROW_DOWN).key_down(Keys.ENTER).perform()
        self.find(By.XPATH, "//ComboBox[contains(@AutomationId, 'CollectionCombobox')]").click()
        ActionChains(self.driver).key_down(Keys.ARROW_DOWN).key_down(Keys.ENTER).perform()
        self.screen(self.driver, 'AfterSelectSetAndCollection')
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'okbutton')]").click()
        WebDriverWait(self.driver, 60).until(EC.invisibility_of_element_located(
            (By.XPATH, "//Custom[contains(@AutomationId, 'MoveToCollectionDialog')]")))
        self.screen(self.driver, 'AfterMoveToOtherCollection')
        # todo: improve function db_selected_collection
        selected_collection_id = vm.db_selected_collection(result)
        return selected_collection_id

    @allure.step('Click [Move to folder], select folder, ok')
    def moveFolderFile(self):
        vm.log().debug('FUNC: moveFolderFile')
        self.find(By.XPATH, "//MenuItem[contains(@Name, 'Move to folder')]").click()
        self.screen(self.driver, 'OpenMoveFolderFileDialog')
        # self.find(By.XPATH, "//ComboBox[contains(@AutomationId, 'folderlist')]").click()
        # ActionChains(self.driver).key_down(Keys.ARROW_DOWN).key_down(Keys.ENTER).perform()
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'MoveToFolderDialog')]"
                            "//Button[contains(@AutomationId, 'okbutton')]").click()
        # WebDriverWait(self.driver, 120).until(EC.invisibility_of_element_located(
        #     (By.XPATH, "//Custom[contains(@AutomationId, 'MoveToFolderDialog')]")))
        self.screen(self.driver, 'AfterClickOkButton')
        return self

    @allure.step('Change View')
    def changeView(self, view='all'):
        vm.log().debug('FUNC: changeView')
        all_views = ['ViewbyList', 'ViewbyTrack', 'ViewbySmall', 'ViewbyMedium', 'ViewbyLarge']
        if view == 'random':
            random.shuffle(all_views)
            v = [all_views.pop()]
            all_views = v
        vm.log().debug(all_views)
        for viewby in all_views:
            self.find(By.XPATH, "//Custom[contains(@AutomationId, 'deta')]"
                                "//Button[contains(@AutomationId, 'ViewbyButton')]").click()
            self.driver.find_element_by_accessibility_id(viewby).click()
            self.screen(self.driver, 'AfterChangeView')

    @allure.step('Change group')
    def changeGroup(self, group='all'):
        vm.log().debug('FUNC: changeGroup')
        all_groups = []
        if group == 'random':
            all_groups.append(random.choice(['GroupbyNone', 'GroupbyDate', 'GroupbyFolder', 'GroupbyType']))
        elif group == 'all':
            all_groups = ['GroupbyNone', 'GroupbyDate', 'GroupbyFolder', 'GroupbyType']
        else:
            all_groups.append(group)
        vm.log().debug(all_groups)
        for groupby in all_groups:
            self.find(By.XPATH, "//Custom[contains(@AutomationId, 'deta')]"
                                "//Button[contains(@AutomationId, 'GroupbyButton')]").click()
            self.driver.find_element_by_accessibility_id(groupby).click()
            self.screen(self.driver, 'AfterChangeGroup')

    @allure.step('Change sort')
    def changeSort(self, sort='all'):
        vm.log().debug('FUNC: changeSort')
        all_sorts = ['SortbyName', 'SortbyDate', 'SortbyFolder', 'SortbyType', 'SortbySize']
        if sort == 'random':
            random.shuffle(all_sorts)
            s = [all_sorts.pop()]
            all_sorts = s
        vm.log().debug(all_sorts)
        for sortby in all_sorts:
            self.find(By.XPATH, "//Custom[contains(@AutomationId, 'deta')]"
                                "//Button[contains(@AutomationId, 'SortbyButton')]").click()
            self.driver.find_element_by_accessibility_id(sortby).click()
            self.screen(self.driver, 'AfterChangeSort')

    @allure.step('Click [Details]')
    def openDetails(self):
        vm.log().debug('FUNC: openDetails')
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'Detailsbutton')]").click()
        self.screen(self.driver, 'openDetails')

    @allure.step('Add assigned keywords')
    def addAssignedKeywords(self):
        vm.log().debug('FUNC: addAssignedKeywords')
        print('open detail')
        elements = self.driver.find_elements_by_xpath(
            "//Custom[contains(@AutomationId, 'ImageDetail')]/Pane/Button[contains(@AutomationId, 'DetailButton')]")
        print(elements)
        elements[0].click()
        print('click +')
        self.screen(self.driver, 'OpenNewAssignedKeywordsDialog')
        n = time.strftime('kw%Y%m%d%H%M%S', time.localtime(time.time()))
        self.find(By.XPATH, "//Edit[contains(@AutomationId, 'EnterName')]").send_keys(n)
        self.screen(self.driver, 'InputKeyword')
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'okbutton')]").click()
        WebDriverWait(self.driver, 60).until(EC.invisibility_of_element_located(
            (By.XPATH, "//Custom[contains(@AutomationId, 'NewKeywordDialog')]")))
        self.screen(self.driver, 'AfterAssignKeyword')
        return n

    @allure.step('Click assigned keywords')
    def clickAssignedKeywords(self, k):
        vm.log().debug('FUNC: clickAssignedKeywords')
        self.find(By.XPATH, "//Button[contains(@Name, '%s')]" % k).click()
        self.screen(self.driver, 'AfterClickAssignedKeyword')

    @allure.step('Click assigned keywords')
    def clickAssignKeywords(self, k):
        vm.log().debug('FUNC: clickAssignKeywords')
        self.find(By.XPATH,
                  "//Custom[contains(@AutomationId, 'MultDetail')]"
                  "//List[contains(@AutomationId, 'assignedlist')]"
                  "//Button[contains(@Name, '%s')]" % k).click()
        self.screen(self.driver, 'AfterClickKeyword')
        return self

    @allure.step('Add suggested keywords')
    def addSuggestedKeywords(self):
        vm.log().debug('FUNC: addSuggestedKeywords')
        elements = self.driver.find_elements_by_xpath(
            "//Custom[contains(@AutomationId, 'ImageDetail')]/Pane/Button[contains(@AutomationId, 'DetailButton')]")
        vm.log().debug(elements)
        elements[1].click()
        self.screen(self.driver, 'OpenAddSuggestedKeywordsDialog')
        n = time.strftime('kw%Y%m%d%H%M%S', time.localtime(time.time()))
        self.find(By.XPATH, "//Edit[contains(@AutomationId, 'EnterName')]").send_keys(n)
        self.screen(self.driver, 'InputAssignedKeyword')
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'okbutton')]").click()
        self.screen(self.driver, 'CompleteAddSuggestedKeywords')
        return n

    @allure.step('Click suggest keyword')
    def clickSuggestKeyword(self, k):
        vm.log().debug('FUNC: clickSuggestKeyword')
        self.find(By.XPATH, "//Button[contains(@Name, '%s')]" % k).click()
        self.screen(self.driver, 'clickSuggestKeyword')

    @allure.step('Remove suggested keywords')
    def removeSuggestKeyword(self, k):
        vm.log().debug('FUNC: removeSuggestKeyword')
        ActionChains(self.driver).context_click(self.find(By.XPATH, "//Button[contains(@Name, '%s')]" % k)).perform()
        self.screen(self.driver, 'BeforeRemoveSuggestKeyword')
        ActionChains(self.driver).key_down(Keys.TAB).key_down(Keys.TAB).key_down(Keys.ENTER).perform()
        self.screen(self.driver, 'AfterRemoveSuggestKeyword')

    @allure.step('Filter files')
    def filter(self):
        vm.log().debug('FUNC: filter')
        current_def = sys._getframe().f_code.co_name
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'Filterbutton')]").click()
        self.find(By.XPATH, "//ListItem[contains(@Name, 'DMAM.Classes.FilterFile')]").click()
        self.screen(self.driver, 'OpenFilter')
        screenshot1 = vm.create_screenshot_path(current_def)
        self.driver.get_screenshot_as_file(screenshot1)

    @allure.step('Open preview')
    def openPreview(self):
        vm.log().debug('FUNC: openPreview')
        ActionChains(self.driver).key_down(Keys.ENTER).perform()
        self.screen(self.driver, 'OpenPreviewByEnter')

    @allure.step('Close preview')
    def closePreview(self):
        vm.log().debug('FUNC: closePreview')
        ActionChains(self.driver).key_down(Keys.ESCAPE).perform()
        self.screen(self.driver, 'ExitPreviewPlayer')

    # @allure.step('zoom in/zoom out')
    # def preview_zoom(self):
    #     vm.log().debug('FUNC: preview_zoom')
    #     current_def = sys._getframe().f_code.co_name
    #     time.sleep(3)
    #     screenshot1 = vm.get_screenshot(current_def)
    #     ActionChains(self.driver).key_down(Keys.ADD).perform()
    #     time.sleep(3)
    #     screenshot2 = vm.get_screenshot(current_def)
    #     ActionChains(self.driver).key_down(Keys.SUBTRACT).perform()
    #     time.sleep(3)
    #     screenshot3 = vm.get_screenshot(current_def)
    #     result_in = cs.compare_image(screenshot1, screenshot2)
    #     result_out = cs.compare_image(screenshot1, screenshot3)
    #     vm.log().debug(result_in)
    #     vm.log().debug(result_out)
    #     if result_out > result_in:
    #         return True
    #     else:
    #         return False

    @allure.step('zoom in/zoom out')
    def preview_zoom(self):
        vm.log().debug('FUNC: preview_zoom')
        current_def = sys._getframe().f_code.co_name
        time.sleep(3)
        screenshot1 = vm.create_screenshot_path(current_def)
        self.driver.get_screenshot_as_file(screenshot1)
        ActionChains(self.driver).key_down(Keys.ADD).perform()
        time.sleep(3)
        self.screen(self.driver, 'ZoomIn')
        screenshot2 = vm.create_screenshot_path(current_def)
        self.driver.get_screenshot_as_file(screenshot2)
        ActionChains(self.driver).key_down(Keys.SUBTRACT).perform()
        time.sleep(3)
        self.screen(self.driver, 'ZoomOut')
        screenshot3 = vm.create_screenshot_path(current_def)
        self.driver.get_screenshot_as_file(screenshot3)
        result_in = cs.compare_image(screenshot1, screenshot2)
        result_out = cs.compare_image(screenshot1, screenshot3)
        vm.log().debug(result_in)
        vm.log().debug(result_out)
        if result_out > result_in:
            return True
        else:
            return False

    @allure.step('rotate left/rotate right')
    def preview_rotate(self):
        vm.log().debug('FUNC: preview_rotate')
        current_def = sys._getframe().f_code.co_name
        time.sleep(3)
        screenshot1 = vm.create_screenshot_path(current_def)
        self.driver.get_screenshot_as_file(screenshot1)
        ActionChains(self.driver).send_keys('l').perform()
        time.sleep(3)
        self.screen(self.driver, 'RotateLeft')
        screenshot2 = vm.create_screenshot_path(current_def)
        self.driver.get_screenshot_as_file(screenshot2)
        ActionChains(self.driver).send_keys('r').perform()
        time.sleep(3)
        self.screen(self.driver, 'RotateRight')
        screenshot3 = vm.create_screenshot_path(current_def)
        self.driver.get_screenshot_as_file(screenshot3)
        result_l = cs.compare_image(screenshot1, screenshot2)
        result_r = cs.compare_image(screenshot1, screenshot3)
        vm.log().debug(result_l)
        vm.log().debug(result_r)
        if result_r > result_l:
            return True
        else:
            return False

    @allure.step('previous file/next file')
    def preview_switch_file(self):
        vm.log().debug('FUNC: preview_switch_file')
        current_def = sys._getframe().f_code.co_name
        time.sleep(3)
        i = 0
        j = 0
        result_previous = ''
        result_next = ''
        screenshot1 = vm.create_screenshot_path(current_def)
        self.driver.get_screenshot_as_file(screenshot1)
        while i < random.randint(1, 10):
            # print('i')
            ActionChains(self.driver).send_keys(Keys.PAGE_UP).perform()
            time.sleep(3)
            self.screen(self.driver, 'PreviousFile')
            screenshot2 = vm.create_screenshot_path(current_def)
            self.driver.get_screenshot_as_file(screenshot2)
            result_previous = cs.compare_image(screenshot1, screenshot2)
            if result_previous > 0.9:
                vm.log().debug(screenshot1)
                vm.log().debug(screenshot2)
                break
            screenshot1 = screenshot2
            i += 1
        while j < random.randint(1, 10):
            # print('j'+ str(j))
            ActionChains(self.driver).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(3)
            self.screen(self.driver, 'NextFile')
            screenshot2 = vm.create_screenshot_path(current_def)
            self.driver.get_screenshot_as_file(screenshot2)
            # if images are same, return True
            result_next = cs.compare_image(screenshot1, screenshot2)
            if result_next > 0.9:
                vm.log().debug(screenshot1)
                vm.log().debug(screenshot2)
                break
            screenshot1 = screenshot2
            j += 1
        if result_previous < 0.9 and result_next < 0.9:
            return True
        else:
            return False

    @allure.step('fullscreen/restore')
    def preview_fullscreen(self):
        vm.log().debug('FUNC: preview_fullscreen')
        current_def = sys._getframe().f_code.co_name
        time.sleep(3)
        screenshot1 = vm.create_screenshot_path(current_def)
        self.driver.get_screenshot_as_file(screenshot1)
        ActionChains(self.driver).send_keys(Keys.F11).perform()
        time.sleep(3)
        self.screen(self.driver, 'FullScreen')
        screenshot2 = vm.create_screenshot_path(current_def)
        self.driver.get_screenshot_as_file(screenshot2)
        ActionChains(self.driver).send_keys(Keys.F11).perform()
        time.sleep(3)
        self.screen(self.driver, 'Restore')
        screenshot3 = vm.create_screenshot_path(current_def)
        self.driver.get_screenshot_as_file(screenshot3)
        result_f = cs.compare_image(screenshot1, screenshot2)
        vm.log().debug(result_f)
        result_r = cs.compare_image(screenshot1, screenshot3)
        vm.log().debug(result_r)
        if result_r > result_f:
            return True
        else:
            return False

    @allure.step('play/stop by SPACE key')
    def preview_play_space(self):
        vm.log().debug('FUNC: preview_play_space')
        current_def = sys._getframe().f_code.co_name
        time.sleep(1)
        screenshot1 = vm.create_screenshot_path(current_def)
        self.driver.get_screenshot_as_file(screenshot1)
        ActionChains(self.driver).send_keys(Keys.SPACE).perform()
        time.sleep(3)
        self.screen(self.driver, 'PressSpaceKey')
        screenshot2 = vm.create_screenshot_path(current_def)
        self.driver.get_screenshot_as_file(screenshot2)
        ActionChains(self.driver).send_keys(Keys.SPACE).perform()
        time.sleep(3)
        self.screen(self.driver, 'PressSpaceKey')
        screenshot3 = vm.create_screenshot_path(current_def)
        self.driver.get_screenshot_as_file(screenshot3)
        # should be different
        result_play = cs.compare_image(screenshot1, screenshot2)
        # should be same
        result_stop = cs.compare_image(screenshot1, screenshot3)
        vm.log().debug("play:"+str(result_play))
        vm.log().debug("stop:"+str(result_stop))
        if result_stop > result_play:
            return True
        else:
            return False

    @allure.step('Play/pause by ENTER key')
    def preview_play_enter(self):
        vm.log().debug('FUNC: preview_play_enter')
        current_def = sys._getframe().f_code.co_name
        time.sleep(1)
        screenshot1 = vm.create_screenshot_path(current_def)
        self.driver.get_screenshot_as_file(screenshot1)
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        time.sleep(3)
        self.screen(self.driver, 'PressEnterKey')
        screenshot2 = vm.create_screenshot_path(current_def)
        self.driver.get_screenshot_as_file(screenshot2)
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        time.sleep(3)
        self.screen(self.driver, 'PressEnterKey')
        screenshot3 = vm.create_screenshot_path(current_def)
        self.driver.get_screenshot_as_file(screenshot3)
        # should be different
        result_play = cs.compare_image(screenshot1, screenshot2)
        # should be different
        result_pause = cs.compare_image(screenshot1, screenshot3)
        vm.log().debug(result_play)
        vm.log().debug(result_pause)
        if result_play < 0.95 and result_pause < 0.95:
            return True
        else:
            return False

    @allure.step('clip in/clip out/reset clip')
    def preview_clip(self):
        vm.log().debug('FUNC: preview_clip')
        current_def = sys._getframe().f_code.co_name
        time.sleep(1)
        screenshot1 = vm.create_screenshot_path(current_def)
        self.driver.get_screenshot_as_file(screenshot1)
        ActionChains(self.driver).send_keys('o').perform()
        time.sleep(3)
        self.screen(self.driver, 'SetOutPoint')
        screenshot2 = vm.create_screenshot_path(current_def)
        self.driver.get_screenshot_as_file(screenshot2)
        ActionChains(self.driver).send_keys('u').perform()
        time.sleep(3)
        self.screen(self.driver, 'ResetRegion')
        screenshot3 = vm.create_screenshot_path(current_def)
        self.driver.get_screenshot_as_file(screenshot3)
        ActionChains(self.driver).send_keys(Keys.END).perform()
        ActionChains(self.driver).send_keys('i').perform()
        time.sleep(3)
        self.screen(self.driver, 'SetInPoint')
        screenshot4 = vm.create_screenshot_path(current_def)
        self.driver.get_screenshot_as_file(screenshot4)
        result_out = cs.compare_image(screenshot1, screenshot2)
        result_reset1 = cs.compare_image(screenshot1, screenshot3)
        result_in = cs.compare_image(screenshot1, screenshot4)
        vm.log().debug(result_out)
        vm.log().debug(result_reset1)
        vm.log().debug(result_in)
        # vm.log().debug(result_reset2)
        # pre of different images is less than similar images
        if result_out < result_reset1 and result_in < result_reset1:
            return True
        else:
            return False

    @allure.step('Mute/unmute')
    def preview_mute(self):
        vm.log().debug('FUNC: preview_mute')
        current_def = sys._getframe().f_code.co_name
        # mute
        ActionChains(self.driver).send_keys('m').perform()
        self.screen(self.driver, 'PressMuteKey')
        time.sleep(1)
        screenshot1 = vm.create_screenshot_path(current_def)
        self.driver.get_screenshot_as_file(screenshot1)
        # unmute
        ActionChains(self.driver).send_keys('m').perform()
        self.screen(self.driver, 'PressMuteKey')
        time.sleep(1)
        screenshot2 = vm.create_screenshot_path(current_def)
        self.driver.get_screenshot_as_file(screenshot2)
        result = cs.compare_image(screenshot1, screenshot2)
        vm.log().debug(result)
        if result < 1:
            return True
        else:
            return False

    # @allure.step('Generate thumbnail automatically')
    # def preview_auto_generate_thumbnail(self):
    #     vm.log().debug('FUNC: preview_generate_thumbnail')
    #     current_def = sys._getframe().f_code.co_name
    #     time.sleep(10)
    #     screenshot1 = vm.create_screenshot_path(current_def)
    #     self.driver.get_screenshot_as_file(screenshot1)
    #     # self.find(By.XPATH, "//Custom[contains(@AutomationId, 'PreviewPlayer')]"
    #     #                     "//Button[contains(@AutomationId, 'MoreButton')]").click()
    #     # self.driver.find_element_by_name('Generate thumbnails').click()
    #     # time.sleep(5)
    #     # screenshot2 = vm.create_screenshot_path(current_def)
    #     # self.driver.get_screenshot_as_file(screenshot2)
    #     # result_thumbnail = cs.compare_image(screenshot1, screenshot2)
    #     # vm.log().debug(result_thumbnail)
    #     # if result_thumbnail < 0.95:
    #     #     return True
    #     # else:
    #     #     return False

    # @allure.step('Generate waveforms')
    # def preview_auto_generate_waveforms(self):
    #     vm.log().debug('FUNC: preview_generate_waveforms')
    #     current_def = sys._getframe().f_code.co_name
    #     time.sleep(3)
    #     screenshot1 = vm.create_screenshot_path(current_def)
    #     self.driver.get_screenshot_as_file(screenshot1)
    #     self.find(By.XPATH, "//Custom[contains(@AutomationId, 'PreviewPlayer')]"
    #                         "//Button[contains(@AutomationId, 'MoreButton')]").click()
    #     self.driver.find_element_by_name('Generate waveforms').click()
    #     time.sleep(5)
    #     screenshot2 = vm.create_screenshot_path(current_def)
    #     self.driver.get_screenshot_as_file(screenshot2)
    #     result_thumbnail = cs.compare_image(screenshot1, screenshot2)
    #     vm.log().debug(result_thumbnail)
    #     if result_thumbnail < 0.95:
    #         return True
    #     else:
    #         return False
