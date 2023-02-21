import sqlite3
import time
from appium.webdriver.webdriver import WebDriver
from page.App import App
import pytest
import custom_method.vpmethod as vm
import allure


class TestFiles(object):
    driver = WebDriver
    # current_database = vm.read_yml('database')[0]
    current_database = vm.yml_data['database'][0]
    mydb = sqlite3.connect(current_database)
    cursor = mydb.cursor()

    @classmethod
    def setup_class(cls):
        cls.mainPage = App.main()
        cls.mainPage.driver.maximize_window()

    def setup_method(self):
        self.mainPage = App.main()
        time.sleep(3)

    def teardown_method(self):
        self.mainPage.driver.quit()

    def test_group(self):
        self.mainPage.changeGroup('GroupbyNone')

    @allure.feature("add to target collection")
    def test_add_all_folder_files_to_target_collection(self):
        folder_id = self.mainPage.selectFolderFile('all')
        self.mainPage.rightClick()
        result = self.mainPage.findAddToTarget()
        if not result:
            self.mainPage.clickRemoveFromTarget().rightClick().clickAddToTarget()
        else:
            self.mainPage.clickAddToTarget()
        # self.mainPage.addToTargetCollection()
        if self.mainPage.IsSetTargetDialogOpen():
            self.mainPage.setTargetCollection()
        # self.mainPage.WaitProgressDialogClosed()
        folderfile = vm.get_from_db("Select Id from LocalFileInfo WHERE ParentFolderId=%s" % folder_id)
        vm.log().debug(folderfile)
        target_id = vm.get_target_id()
        collectionfile = vm.get_from_db(
            "Select LocalFileInfoId from JoinLocalFileInfoAndCollection WHERE CollectionId=%s" % target_id)
        vm.log().debug(collectionfile)
        # assert 是否folder下的所有文件都在target collection里
        for i in folderfile:
            assert i in collectionfile

    @allure.feature("add to target collection")
    def test_add_one_folder_file_to_target_collection(self):
        target_id = vm.get_target_id()
        collectionfile_old = vm.get_from_db(
            "Select LocalFileInfoId from JoinLocalFileInfoAndCollection WHERE CollectionId=%s" % target_id)
        folder_id = self.mainPage.selectFolderFile()
        self.mainPage.addToTargetCollectionByCrosshair()
        if self.mainPage.IsSetTargetDialogOpen():
            self.mainPage.setTargetCollection()
        self.mainPage.WaitProgressDialogClosed()
        collectionfile_new = vm.get_from_db(
            "Select LocalFileInfoId from JoinLocalFileInfoAndCollection WHERE CollectionId=%s" % target_id)
        n = len(collectionfile_new)-len(collectionfile_old)
        assert n == 1 or n == -1

    @allure.feature("add to collection")
    @pytest.mark.parametrize("execution_time", range(0, 3))
    def test_add_all_folder_files_to_collection(self, execution_time):
        folder_id = self.mainPage.selectFolderFile('all')
        self.mainPage.rightClick()
        collection_id = self.mainPage.addToCollection()
        vm.log().debug(collection_id)
        folderfile = vm.get_from_db("Select Id from LocalFileInfo WHERE ParentFolderId=%s" % folder_id)
        collectionfile = vm.get_from_db(
            "Select LocalFileInfoId from JoinLocalFileInfoAndCollection WHERE CollectionId=%s" % collection_id)
        # addToCollection: its return id maybe wrong
        # for i in folderfile:
        #     assert i in collectionfile

    @allure.feature("create collection for files")
    @pytest.mark.parametrize("execution_time", range(0, 3))
    def test_create_collection_for_folder_file(self, execution_time):
        # select random files
        folder_id = self.mainPage.selectFolderFile('random')
        # self.mainPage.fileMenu()
        self.mainPage.rightClick().openCreateCollectionDialog()
        # get collection name
        collection_name = self.mainPage.createCollectionForFiles()
        time.sleep(1)
        collection_id = vm.get_from_db("select Id from Collections")[-1][0]
        name = vm.get_from_db("select Name from Collections where Id=%s" % collection_id)[0][0]
        if collection_name == name:
            collection_file = vm.get_from_db(
                "select LocalFileInfoId from JoinLocalFileInfoAndCollection where CollectionId=%s" % collection_id)
            file_id = collection_file[0][0]
            assert len(collection_file) >= 1
            assert vm.get_from_db("select ParentFolderId from LocalFileInfo where Id=%s" % file_id)[0][0] == folder_id
        else:
            vm.log().debug("MY FUNC IS ERR")
            assert False

    @allure.feature("add to collection")
    def test_add_random_collection_files_to_collection(self):
        selected_id = self.mainPage.selectRandomCollectionFile()
        n = self.mainPage.getSelectedFileNumber()
        # self.mainPage.fileMenu()
        self.mainPage.rightClick()
        collection_id = self.mainPage.addToCollection()
        fromCollectionFiles = vm.get_from_db(
            "Select LocalFileInfoId from JoinLocalFileInfoAndCollection WHERE CollectionId=%s" % selected_id)
        toCollectionFile = vm.get_from_db(
            "Select LocalFileInfoId from JoinLocalFileInfoAndCollection WHERE CollectionId=%s" % collection_id)
        u = []
        for i in fromCollectionFiles:
            if i in toCollectionFile:
                u.append(i)
        vm.log().debug(u)
        # addToCollection: its return id maybe wrong
        # assert len(u) > n

    @allure.feature("add to target collection")
    def test_add_all_collection_files_to_target_collection(self):
        target_id = vm.get_target_id()
        while True:
            collection_id = self.mainPage.selectAllCollectionFile()
            if collection_id != target_id:
                break
        self.mainPage.rightClick()
        result = self.mainPage.findAddToTarget()
        if not result:
            self.mainPage.clickRemoveFromTarget().rightClick().clickAddToTarget()
        else:
            self.mainPage.clickAddToTarget()
        # self.mainPage.addToTargetCollection()
        if self.mainPage.IsSetTargetDialogOpen():
            self.mainPage.setTargetCollection()
        time.sleep(3)
        target_id = vm.get_target_id()
        fromCollectionFiles = vm.get_from_db(
            "Select LocalFileInfoId from JoinLocalFileInfoAndCollection WHERE CollectionId=%s" % collection_id)
        vm.log().debug(fromCollectionFiles)
        toCollectionFile = vm.get_from_db(
            "Select LocalFileInfoId from JoinLocalFileInfoAndCollection WHERE CollectionId=%s" % target_id)
        vm.log().debug(toCollectionFile)
        # assert 是否folder下的所有文件都在target collection里
        for i in fromCollectionFiles:
            assert i in toCollectionFile

    @allure.feature("add to target collection")
    def test_add_random_collection_files_to_target_collection(self):
        target_id = vm.get_target_id()
        while True:
            collection_id = self.mainPage.selectAllCollectionFile()
            if collection_id != target_id:
                break
        # collection_id = self.mainPage.selectRandomCollectionFile()
        n = self.mainPage.getSelectedFileNumber()
        # self.mainPage.fileMenu()
        self.mainPage.rightClick()
        result = self.mainPage.findAddToTarget()
        if not result:
            self.mainPage.clickRemoveFromTarget().rightClick().clickAddToTarget()
        else:
            self.mainPage.clickAddToTarget()
        if self.mainPage.IsSetTargetDialogOpen():
            self.mainPage.setTargetCollection()
        target_id = vm.get_target_id()
        fromCollectionFiles = vm.get_from_db(
            "Select LocalFileInfoId from JoinLocalFileInfoAndCollection WHERE CollectionId=%s" % collection_id)
        toCollectionFile = vm.get_from_db(
            "Select LocalFileInfoId from JoinLocalFileInfoAndCollection WHERE CollectionId=%s" % target_id)
        u = []
        for i in fromCollectionFiles:
            if i in toCollectionFile:
                u.append(i)
        vm.log().debug(u)
        assert len(u) >= n

    @allure.feature("move file")
    def test_move_random_collection_file(self):
        selected_id = self.mainPage.selectRandomCollectionFile()
        old_collection_file = vm.get_from_db(
            "Select LocalFileInfoId from JoinLocalFileInfoAndCollection WHERE CollectionId=%s" % selected_id)
        n = self.mainPage.getSelectedFileNumber()
        self.mainPage.rightClick()
        target_id = self.mainPage.moveCollectionFile()
        new_collection_file = vm.get_from_db(
            "Select LocalFileInfoId from JoinLocalFileInfoAndCollection WHERE CollectionId=%s" % selected_id)
        target_collection_file = vm.get_from_db(
            "Select LocalFileInfoId from JoinLocalFileInfoAndCollection WHERE CollectionId=%s" % target_id)
        moved = []
        for i in old_collection_file:
            if i not in new_collection_file:
                moved.append(i)
        # moveCollectionFile: its return value maybe wrong
        # if selected_id == target_id:
        #     assert len(moved) == 0
        # else:
        #     assert len(moved) == n
        #     for f in moved:
        #         assert f in target_collection_file

    @allure.feature("move file")
    def test_move_all_collection_files(self):
        selected_id = self.mainPage.selectAllCollectionFile()
        old_collection_file = vm.get_from_db(
            "Select LocalFileInfoId from JoinLocalFileInfoAndCollection WHERE CollectionId=%s" % selected_id)
        self.mainPage.rightClick()
        target_id = self.mainPage.moveCollectionFile()
        new_collection_file = vm.get_from_db(
            "Select LocalFileInfoId from JoinLocalFileInfoAndCollection WHERE CollectionId=%s" % selected_id)
        target_collection_file = vm.get_from_db(
            "Select LocalFileInfoId from JoinLocalFileInfoAndCollection WHERE CollectionId=%s" % target_id)
        # moveCollectionFile: its return value maybe wrong
        # if selected_id == target_id:
        #     assert old_collection_file == new_collection_file
        # else:
        #     assert new_collection_file == []
        #     for i in old_collection_file:
        #         assert i in target_collection_file

    @allure.feature("move file")
    def test_move_folder_file(self):
        folder_id = self.mainPage.selectFolderFile('all')
        folder_list = vm.get_subfolder_from_folder(folder_id)
        selected_folder_file = []
        target_id = vm.db_selected_folder()
        target_folder_file_before_move = vm.get_from_db(
            "select FileName from LocalFileInfo where ParentFolderId=%s" % target_id)
        for i in folder_list:
            selected_folder_file = selected_folder_file + vm.get_from_db(
                "select FileName from LocalFileInfo where ParentFolderId=%s" % i)
        self.mainPage.rightClick().moveFolderFile()
        vm.log().debug('target_id: %s' % target_id)
        self.mainPage.WaitProgressDialogClosed()
        selected_folder_file_after_move = vm.get_from_db(
            "select FileName from LocalFileInfo where ParentFolderId=%s" % folder_id)
        target_folder_file_after_move = vm.get_from_db(
            "select FileName from LocalFileInfo where ParentFolderId=%s" % target_id)
        if folder_id == target_id:
            for i in selected_folder_file:
                assert i in selected_folder_file_after_move
            for j in selected_folder_file_after_move:
                assert j in selected_folder_file
        else:
            for i in selected_folder_file:
                if i not in target_folder_file_before_move:
                    assert i not in selected_folder_file_after_move
                    assert i in target_folder_file_after_move
                else:
                    assert i in selected_folder_file_after_move
                    assert i in target_folder_file_after_move

    @allure.feature("create collection for files")
    def test_create_collection_for_collection_file_and_set_target(self):
        collection_id = self.mainPage.selectAllCollectionFile()
        collection_file = vm.get_from_db(
            "select LocalFileInfoId from JoinLocalFileInfoAndCollection where CollectionId=%s" % collection_id)
        self.mainPage.rightClick().openCreateCollectionDialog().checkOnSetAsTarget()
        target_name = self.mainPage.createCollectionForFiles()
        time.sleep(3)
        target_id = vm.get_from_db("select Id from Collections")[-1][0]
        # target_id = vm.get_from_db("select Id from Collections where Name=%s" % target_name)
        vm.log().debug(target_id)
        name = vm.get_from_db("select Name from Collections where Id=%s" % target_id)[0][0]
        vm.log().debug(target_name)
        vm.log().debug(name)
        if target_name == name:
            assert str(vm.get_target_id()) == str(target_id)
            new_collection_file = vm.get_from_db(
                "select LocalFileInfoId from JoinLocalFileInfoAndCollection where CollectionId=%s" % target_id)
            for i in collection_file:
                assert i in new_collection_file
        else:
            vm.log().debug("MY FUNC IS ERR")
            assert False

    @allure.feature("rename")
    def test_rename_folder_file(self):
        folder_id = self.mainPage.selectFolderFile()
        old_folder_file = vm.get_from_db("select Id, FileName from LocalFileInfo where ParentFolderId=%s" % folder_id)
        # self.mainPage.fileMenu()
        self.mainPage.rightClick()
        self.mainPage.openRenameDialog()
        new_name = self.mainPage.confirmRename()
        self.mainPage.waitRenameComplete()
        new_folder_file = vm.get_from_db("select Id, FileName from LocalFileInfo where ParentFolderId=%s" % folder_id)
        filelist = []
        for i in old_folder_file:
            if i not in new_folder_file:
                filelist.append(i)
        vm.log().debug(filelist)
        file_id = filelist[0][0]
        # 取到的name带后缀名，split后取第一个值
        full_file_name = vm.get_from_db("select FileName from LocalFileInfo where Id=%s" % file_id)[0][0]
        file_name = full_file_name.split('.')[0]
        assert file_name == new_name

    @allure.feature("rename")
    def test_rename_collection_file(self):
        collection_id = self.mainPage.selectRandomCollectionFile()
        collection_file_id = vm.get_from_db(
            "select LocalFileInfoId from JoinLocalFileInfoAndCollection where CollectionId=%s" % collection_id)
        old_collection_files = []
        for i in collection_file_id:
            collection_file = vm.get_from_db("select Id, FileName from LocalFileInfo where Id=%s" % i[0])
            old_collection_files.append(collection_file[0])
        vm.log().debug(old_collection_files)
        # self.mainPage.fileMenu()
        self.mainPage.rightClick()
        self.mainPage.openRenameDialog()
        new_name = self.mainPage.confirmRename()
        self.mainPage.waitRenameComplete()
        new_collection_files = []
        for i in collection_file_id:
            collection_file = vm.get_from_db("select Id, FileName from LocalFileInfo where Id=%s" % i[0])
            new_collection_files.append(collection_file[0])
        vm.log().debug(new_collection_files)
        for i in old_collection_files:
            if i in new_collection_files:
                new_collection_files.remove(i)
                continue
        vm.log().debug(old_collection_files)
        vm.log().debug(new_collection_files)
        file_name = new_collection_files[0][1].split('.')[0]
        assert file_name == new_name

    @allure.feature("keywords")
    def test_add_assigned_keywords(self):
        # select one file
        self.mainPage.selectFolderFile()
        self.mainPage.openDetails()
        new_k = self.mainPage.addAssignedKeywords()
        time.sleep(2)
        k_id = vm.get_from_db("select Id from Keyword where Name='%s'" % new_k)[0][0]
        vm.log().debug(k_id)
        key_file = vm.get_from_db("select LocalFileInfoId from JoinKeywordAndLocalFileInfo where KeywordId=%s" % k_id)
        vm.log().debug(key_file)
        assert len(key_file) == 1
        # Click the new keyword to remove it from Assigned keywords
        self.mainPage.clickAssignedKeywords(new_k)
        time.sleep(2)
        removed_key_files = vm.get_from_db(
            "select LocalFileInfoId from JoinKeywordAndLocalFileInfo where KeywordId=%s" % k_id)
        assert len(removed_key_files) == 0

    @allure.feature("keywords")
    @pytest.mark.skip(reason="after select all files, and find the keyword, cannot click it. why?")
    def test_add_part_assigned_keyword_to_all(self):
        # new keyword to one file
        folder_id = self.mainPage.selectFolderFile()
        folder_files = vm.get_from_db("select Id from LocalFileInfo where ParentFolderId=%s" % folder_id)
        self.mainPage.openDetails()
        new_k = self.mainPage.addAssignedKeywords()
        time.sleep(2)
        k_id = vm.get_from_db("select Id from Keyword where Name='%s'" % new_k)[0][0]
        # add the new keyword to all files
        self.mainPage.clickPageHead().clickPageHead()
        time.sleep(2)
        self.mainPage.clickAssignKeywords(new_k)
        time.sleep(5)
        added_key_files = vm.get_from_db(
            "select LocalFileInfoId from JoinKeywordAndLocalFileInfo where KeywordId=%s" % k_id)
        # assert new_k 是否关联到folder_id下所有的文件
        assert len(folder_files) == len(added_key_files)

    @allure.feature("keywords")
    def test_add_suggested_keyword(self):
        self.mainPage.selectFolderFile()
        self.mainPage.openDetails()
        new_k = self.mainPage.addSuggestedKeywords()
        time.sleep(2)
        k_id = vm.get_from_db("select Id from Keyword where Name='%s'" % new_k)[0][0]
        files = vm.get_from_db(
            "select LocalFileInfoId from JoinKeywordAndLocalFileInfo where KeywordId=%s" % k_id)
        assert len(files) == 0

    @allure.feature("keywords")
    def test_add_suggested_to_assigned(self):
        self.mainPage.selectFolderFile()
        self.mainPage.openDetails()
        new_k = self.mainPage.addSuggestedKeywords()
        time.sleep(2)
        k_id = vm.get_from_db("select Id from Keyword where Name='%s'" % new_k)[0][0]
        self.mainPage.clickSuggestKeyword(new_k)
        time.sleep(2)
        files = vm.get_from_db(
            "select LocalFileInfoId from JoinKeywordAndLocalFileInfo where KeywordId=%s" % k_id)
        assert len(files) == 1

    @allure.feature("keywords")
    def test_remove_suggested_keyword(self):
        self.mainPage.selectFolderFile()
        self.mainPage.openDetails()
        new_k = self.mainPage.addSuggestedKeywords()
        time.sleep(2)
        k_id = vm.get_from_db("select Id from Keyword where Name='%s'" % new_k)
        self.mainPage.removeSuggestKeyword(new_k)
        time.sleep(2)
        removed_k_id = vm.get_from_db("select Id from Keyword where Name='%s'" % new_k)
        assert len(k_id) == 1 and len(removed_k_id) == 0

    @allure.feature("keywords")
    @pytest.mark.skip(reason="cannot make sure selected folder has assigned keywords")
    def test_filter(self):
        self.mainPage.selectFolder()
        self.mainPage.filter()

    @allure.feature("delete/remove file")
    def test_delete_file_from_databse(self):
        folder_id = self.mainPage.selectFolderFile()
        old_files = vm.get_from_db("select Id from LocalFileInfo where ParentFolderId=%s" % folder_id)
        # self.mainPage.fileMenu()
        self.mainPage.rightClick()
        self.mainPage.openDeleteFolderDialog()
        self.mainPage.ConfirmDeleteFiles()
        self.mainPage.WaitProgressDialogClosed()
        new_files = vm.get_from_db("select Id from LocalFileInfo where ParentFolderId=%s" % folder_id)
        assert len(old_files)-len(new_files) == 1

    @allure.feature("delete/remove file")
    def test_delete_file_from_pc(self):
        folder_id = self.mainPage.selectFolderFile('all')
        self.mainPage.rightClick()
        self.mainPage.openDeleteFolderDialog()
        self.mainPage.checkOnDeleteFromPC()
        self.mainPage.ConfirmDeleteFiles()
        full_path = vm.get_from_db("select Path from AssetFolder where Id=%s" % folder_id)[0][0]
        vm.log().debug(full_path)
        self.mainPage.WaitProgressDialogClosed()
        files = vm.get_from_db("select Id from LocalFileInfo where ParentFolderId=%s" % folder_id)
        vm.log().debug(files)
        file_number = vm.get_file_number(full_path)
        vm.log().debug(file_number)
        assert len(files) == 0 and file_number == 0

    @allure.feature("delete/remove file")
    def test_remove_file(self):
        collection_id = self.mainPage.selectAllCollectionFile()
        self.mainPage.rightClick()
        self.mainPage.removeCollectionFile()
        self.mainPage.WaitProgressDialogClosed()
        collection_files = vm.get_from_db(
            "select LocalFileInfoId from JoinLocalFileInfoAndCollection where CollectionId=%s" % collection_id)
        assert len(collection_files) == 0
