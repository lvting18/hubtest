# -*- coding: utf-8 -*-
# coding : utf-8
import time
import pytest
from appium.webdriver.webdriver import WebDriver
from page.App import App
import custom_method.vpmethod as vm
import allure


class TestImport(object):
    driver = WebDriver
    vm.ini_vp()
    # _ini_target = vm.read_yml('import_target')
    _ini_target = vm.yml_data['import_target']
    _test_view_group_sort = vm.load_param('TestImport', 'test_view_group_sort')
    _test_source_mtp = vm.load_param('TestImport', 'test_source_mtp')
    _test_source_removable_disk = vm.load_param('TestImport', 'test_source_removable_disk')
    _test_source_network_drive = vm.load_param('TestImport', 'test_source_network_drive')
    _test_source_empty_folder = vm.load_param('TestImport', 'test_source_empty_folder')
    _test_source_multifile = vm.load_param('TestImport', 'test_source_multifile')
    _test_source_wholefolder = vm.load_param('TestImport', 'test_source_wholefolder')
    _test_source_large = vm.load_param('TestImport', 'test_source_large')
    _test_import_to_existing_target = vm.load_param('TestImport', 'test_import_to_existing_target')
    _test_import_to_library = vm.load_param('TestImport', 'test_import_to_library')

    @classmethod
    def setup_class(cls):
        cls.mainPage = App.main()
        # cls.mainPage.driver.maximize_window()
        time.sleep(3)
        # cls.ImportPage = cls.mainPage.gotoImport()

    def setup_method(self):
        self.ImportPage = self.mainPage.gotoImport()
    #     # self.ImportPage.iniImport()

    def teardown_method(self):
        self.ImportPage.backtomain()

    def teardown_class(self):
        self.mainPage.driver.quit()

    @allure.feature("Change view/group/sort")
    @allure.description('test all view/group/sort')
    @pytest.mark.parametrize(("s",), _test_view_group_sort)
    def test_view_group_sort(self, s):
        vm.log().debug('CASE: test_view_group_sort')
        self.ImportPage.SelectSourceFolder(s)
        self.ImportPage.ClickIncludeSubFolder()
        self.ImportPage.ChangeView()
        self.ImportPage.ChangeGroup()
        self.ImportPage.ChangeSort()
        self.ImportPage.ClickIncludeSubFolder()

    @allure.feature("Import source")
    @allure.description('import mtp device to new target folder')
    @pytest.mark.skip(reason='no mtp device')
    @pytest.mark.parametrize(("s",), _test_source_mtp)
    def test_source_mtp(self, s):
        vm.log().debug('CASE: test_source_mtp')
        s_number = self.ImportPage.SelectMTP(s).GetSelectedFilesNumber()
        t = self.ImportPage.NewTargetFolder(self._ini_target)
        self.ImportPage.ClickImport()
        assert self.ImportPage.IsImportDialogOpen() is True
        self.ImportPage.WaitingImportFinish()
        self.ImportPage.CloseImportDialog()
        assert vm.get_file_number(t) == s_number

    @allure.feature("Import source")
    @pytest.mark.parametrize(("s",), _test_source_removable_disk)
    def test_source_removable_disk(self, s):
        vm.log().debug('CASE: test_source_removable_disk')
        s_number = self.ImportPage.SelectSourceFolder(s).GetSelectedFilesNumber()
        t = self.ImportPage.NewTargetFolder(self._ini_target)
        self.ImportPage.ClickImport()
        self.ImportPage.WaitingImportFinish()
        self.ImportPage.CloseImportDialog()
        assert vm.get_file_number(t) == s_number

    @allure.feature("Import source")
    @pytest.mark.parametrize(("s",), _test_source_network_drive)
    def test_source_network_drive(self, s):
        vm.log().debug('CASE: test_source_network_drive')
        s_number = self.ImportPage.SelectSourceFolder(s).GetSelectedFilesNumber()
        t = self.ImportPage.NewTargetFolder(self._ini_target)
        self.ImportPage.ClickImport()
        self.ImportPage.WaitingImportFinish()
        self.ImportPage.CloseImportDialog()
        assert vm.get_file_number(t) == s_number

    @allure.feature("Import source")
    @allure.description('import empty folder to new target folder, import button is disabled')
    @pytest.mark.parametrize(("s",), _test_source_empty_folder)
    def test_source_empty_folder(self, s):
        vm.log().debug('CASE: test_source_empty_folder')
        self.ImportPage.SelectSourceFolder(s)
        self.ImportPage.NewTargetFolder(self._ini_target)
        self.ImportPage.ClickImport()
        assert self.ImportPage.IsImportDialogOpen() is False

    @allure.feature("Import source")
    @pytest.mark.parametrize(("s",), _test_source_multifile)
    def test_source_multifile(self, s):
        vm.log().debug('CASE: test_source_multifile')
        s_number = self.ImportPage.SelectFile(s).GetSelectedFilesNumber()
        self.ImportPage.GetSelectedFilesNumber()
        t = self.ImportPage.NewTargetFolder(self._ini_target)
        self.ImportPage.ClickImport()
        self.ImportPage.WaitingImportFinish()
        self.ImportPage.CloseImportDialog()
        assert vm.get_file_number(t) == s_number

    @allure.feature("Import source")
    @allure.description('import several files to new target folder')
    @pytest.mark.parametrize(("s", "t"), _test_source_wholefolder)
    def test_source_wholefolder(self, s, t):
        vm.log().debug('CASE: test_source_wholefolder')
        s_number = self.ImportPage.SelectSourceFolder(s).GetSelectedFilesNumber()
        t_path = self.ImportPage.NewTargetFolder(self._ini_target, target_name=t)
        self.ImportPage.ClickImport()
        self.ImportPage.WaitingImportFinish()
        self.ImportPage.CloseImportDialog()
        assert vm.get_file_number(t_path) == s_number

    @allure.feature("Import source")
    @pytest.mark.skip(reason='no need test every time')
    @pytest.mark.parametrize(("s",), _test_source_large)
    def test_source_large(self, s):
        vm.log().debug('CASE: test_source_large')
        s_number = self.ImportPage.SelectSourceFolder(s).GetSelectedFilesNumber()
        t = self.ImportPage.NewTargetFolder(self._ini_target)
        self.ImportPage.ClickImport()
        self.ImportPage.WaitingImportFinish()
        self.ImportPage.CloseImportDialog()
        assert vm.get_file_number(t) == s_number

    @allure.feature("Import target")
    @allure.description('import to existing target')
    @pytest.mark.parametrize(("s", "t"), _test_import_to_existing_target)
    def test_import_to_existing_target(self, s, t):
        vm.log().debug('CASE: test_import_to_existing_target')
        s_number = self.ImportPage.SelectSourceFolder(s).GetSelectedFilesNumber()
        self.ImportPage.SelectTargetFolder(t)
        self.ImportPage.ClickImport()
        self.ImportPage.WaitingImportFinish()
        self.ImportPage.CloseImportDialog()
        assert vm.get_file_number(t) == s_number

    @allure.feature("Import target")
    @allure.description('import to library without target folder')
    @pytest.mark.parametrize(("s",), _test_import_to_library)
    def test_import_to_library(self, s):
        vm.log().debug('CASE: test_import_to_library')
        self.ImportPage.SelectSourceFolder(s)
        time.sleep(3)
        s_number = self.ImportPage.GetSelectedFilesNumber()
        self.ImportPage.ClickAddToLibrary()
        self.ImportPage.WaitingAddFinish()
        self.ImportPage.CloseAddDialog()
        assert vm.get_file_number(s) == s_number

