import os
import time
from appium.webdriver.webdriver import WebDriver
from page.App import App
import pytest
import allure
import custom_method.vpmethod as vm


class TestLibrary(object):
    driver = WebDriver
    _test_add_root_folder = vm.load_param('TestLibrary', 'test_add_root_folder')
    _test_create_folder_multi_lan = vm.load_param('TestLibrary', 'test_create_folder_multi_lan')
    _test_create_folder_failed = vm.load_param('TestLibrary', 'test_create_folder_failed')
    _test_rename_failed = vm.load_param('TestLibrary', 'test_rename_failed')

    @classmethod
    def setup_class(cls):
        cls.mainPage = App.main()
        cls.mainPage.driver.maximize_window()

    def setup_method(self):
        self.mainPage = App.main()
        time.sleep(3)

    def teardown_method(self):
        self.mainPage.driver.quit()

    # def teardown_class(self):
    #     self.mainPage.driver.quit()

    @allure.feature('Prepare')
    def test_random_view_group_sort(self):
        vm.log().debug('CASE: test_random_view_group_sort')
        time.sleep(3)
        self.mainPage.selectFolder()
        self.mainPage.changeView('random')
        self.mainPage.changeGroup('random')
        self.mainPage.changeSort('random')

    @allure.feature("add root folder")
    @pytest.mark.parametrize(('r_path', ), _test_add_root_folder)
    def test_add_root_folder(self, r_path):
        vm.log().debug('CASE: test_add_root_folder')
        self.mainPage.addRootFolder(r_path)
        time.sleep(1)
        tables = vm.get_from_db("select Path from AssetFolder WHERE Path='%s';" % r_path)
        assert tables[0][0] == r_path
        vm.log().debug("just test")

    @allure.feature("add to target collection")
    def test_cancel_add_to_target_collection(self):
        vm.log().debug('CASE: test_cancel_add_to_target_collection')
        self.mainPage.selectFolder()
        self.mainPage.rightClick()
        self.mainPage.clickAddToTarget()
        if self.mainPage.IsSetTargetDialogOpen():
            self.mainPage.closeSetTargetCollectionDialog()

    @allure.feature("add to target collection")
    def test_set_and_add_to_target_collection(self):
        vm.log().debug('CASE: test_set_and_add_to_target_collection')
        folder_id = self.mainPage.selectFolder()
        self.mainPage.rightClick()
        self.mainPage.clickAddToTarget()
        if self.mainPage.IsSetTargetDialogOpen():
            self.mainPage.setTargetCollection()
        time.sleep(5)
        target_id = vm.get_target_id()
        folder_file = vm.get_from_db("select Id from LocalFileInfo WHERE ParentFolderId=%s;" % folder_id)
        vm.log().debug(folder_file)
        collection_file = vm.get_from_db(
            "select LocalFileInfoId from JoinLocalFileInfoAndCollection WHERE CollectionId=%s;" % target_id)
        vm.log().debug(collection_file)
        for i in folder_file:
            assert i in collection_file

    @allure.feature("add to target collection")
    def test_add_folder_to_existing_target_collection(self):
        vm.log().debug('CASE: test_add_folder_to_existing_target_collection')
        folder_id = self.mainPage.selectFolder()
        self.mainPage.folderMenu()
        # self.mainPage.rightClick()
        self.mainPage.clickAddToTarget()
        if self.mainPage.IsSetTargetDialogOpen():
            self.mainPage.setTargetCollection()
        time.sleep(5)
        target_id = vm.get_target_id()
        folder_file = vm.get_from_db("select Id from LocalFileInfo WHERE ParentFolderId=%s;" % folder_id)
        collection_file = vm.get_from_db(
            "select LocalFileInfoId from JoinLocalFileInfoAndCollection WHERE CollectionId=%s;" % target_id)
        for i in folder_file:
            assert i in collection_file

    @allure.feature("create folder")
    def test_create_folder_successfully(self):
        vm.log().debug('CASE: test_create_folder_successfully')
        p_id = self.mainPage.selectFolder()
        self.mainPage.rightClick()
        self.mainPage.openCreateFolderDailog()
        f_name = self.mainPage.confirmCreateFolder()
        self.mainPage.waitCreateFolderComplete()
        p_folder = vm.get_from_db("select Name from AssetFolder WHERE ParentFolderId=%s;" % p_id)
        assert (f_name,) in p_folder

    @allure.feature("create folder")
    @allure.description('Chinese, Arabic, Czech, Japanese, Korean')
    @pytest.mark.parametrize(('s',), _test_create_folder_multi_lan)
    def test_create_folder_multi_lan(self, s):
        vm.log().debug('CASE: test_create_folder_multi_lan')
        p_id = self.mainPage.selectFolder()
        # self.mainPage.rightClick()
        self.mainPage.folderMenu()
        self.mainPage.openCreateFolderDailog()
        self.mainPage.confirmCreateFolder(s)
        self.mainPage.waitCreateFolderComplete()
        p_folder = vm.get_from_db("select Name from AssetFolder WHERE ParentFolderId=%s;" % p_id)
        assert (s,) in p_folder

    @allure.feature("create folder")
    @pytest.mark.parametrize(('s', 'm'), _test_create_folder_failed)
    def test_create_folder_failed(self, s, m):
        vm.log().debug('CASE: test_create_folder_failed')
        self.mainPage.selectFolder()
        self.mainPage.rightClick()
        self.mainPage.openCreateFolderDailog()
        self.mainPage.confirmCreateFolder(s)
        get_m = self.mainPage.getCreateFolderErr()
        vm.log().debug(get_m)
        self.mainPage.closeCreateFolderDialog()
        assert (m in get_m)

    @allure.feature("create folder")
    def test_cancel_create_folder(self):
        vm.log().debug('CASE: test_cancel_create_folder')
        self.mainPage.selectFolder()
        self.mainPage.rightClick()
        self.mainPage.openCreateFolderDailog()
        self.mainPage.closeCreateFolderDialog()

    @allure.feature("rename folder")
    def test_rename(self):
        vm.log().debug('CASE: test_rename')
        folder_id = self.mainPage.selectFolder()
        # self.mainPage.rightClick()
        self.mainPage.folderMenu()
        self.mainPage.openRenameDialog()
        new_name = self.mainPage.confirmRename()
        self.mainPage.waitRenameComplete()
        tables = vm.get_from_db("select Name from AssetFolder WHERE Id=%s;" % folder_id)
        assert tables[0][0] == new_name

    @allure.feature("rename folder")
    @pytest.mark.parametrize(('s', 'm'), _test_rename_failed)
    def test_rename_failed(self, s, m):
        vm.log().debug('CASE: test_rename_failed')
        self.mainPage.selectFolder()
        self.mainPage.rightClick()
        self.mainPage.openRenameDialog()
        self.mainPage.confirmRename(s)
        get_m = self.mainPage.getRenameErr()
        self.mainPage.closeRenameDialog()
        assert (m in get_m)

    @allure.feature("rename folder")
    def test_cancel_rename(self):
        vm.log().debug('CASE: test_cancel_rename')
        self.mainPage.selectFolder()
        self.mainPage.rightClick()
        self.mainPage.openRenameDialog()
        self.mainPage.closeRenameDialog()

    @allure.feature("delete folder")
    def test_delete_folder_from_database(self):
        vm.log().debug('CASE: test_delete_folder_from_database')
        folder_id = self.mainPage.selectFolder()
        # self.mainPage.rightClick()
        self.mainPage.folderMenu()
        self.mainPage.openDeleteFolderDialog()
        self.mainPage.confirmDeleteFolder().waitDeleteFolderFromDbCompleted()
        folder_table = vm.get_from_db("select Name from AssetFolder WHERE Id=%s;" % folder_id)
        file_table = vm.get_from_db("select Id from LocalFileInfo WHERE ParentFolderId=%s;" % folder_id)
        vm.log().debug(folder_table)
        vm.log().debug(file_table)
        assert folder_table == [] and file_table == []

    @allure.feature("delete folder")
    def test_delete_folder_from_pc(self):
        vm.log().debug('CASE: test_delete_folder_from_pc')
        folder_id = self.mainPage.selectFolder()
        folder_path = vm.get_from_db("select Path from AssetFolder WHERE Id=%s;" % folder_id)[0][0]
        vm.log().debug(folder_path)
        file_table = vm.get_from_db("select Id from LocalFileInfo WHERE ParentFolderId=%s;" % folder_id)
        file_db_number = len(file_table)
        vm.log().debug(file_db_number)
        file_number = len(vm.get_files(folder_path))
        self.mainPage.rightClick()
        self.mainPage.openDeleteFolderDialog()
        self.mainPage.checkOnDeleteFromPC()
        self.mainPage.confirmDeleteFolder().waitDeleteFromPcCompleted()
        new_folder_table = vm.get_from_db("select Name from AssetFolder WHERE Id=%s;" % folder_id)
        new_file_table = vm.get_from_db("select Id from LocalFileInfo WHERE ParentFolderId=%s;" % folder_id)
        vm.log().debug(new_folder_table)
        vm.log().debug(new_file_table)
        if os.path.exists(folder_path):
            new_file_number = len(vm.get_files(folder_path))
            n = file_number - new_file_number
            vm.log().debug(n)
            if n == file_db_number:
                allDeleted = True
            else:
                allDeleted = False
        else:
            allDeleted = True
        assert new_folder_table == [] and new_file_table == [] and allDeleted

    @allure.feature("delete folder")
    def test_cancel_delete_folder(self):
        vm.log().debug('CASE: test_cancel_delete_folder')
        folder_id = self.mainPage.selectFolder()
        self.mainPage.rightClick()
        self.mainPage.openDeleteFolderDialog()
        self.mainPage.closeDeleteFolderDialog()

    # @allure.feature("export")
    # @pytest.mark.skip(reason="not implemented")
    # def test_export_library(self):
    #     vm.log().debug('CASE: test_export_library')
    #     pass

