import time
from appium.webdriver.webdriver import WebDriver
from page.App import App
import pytest
import custom_method.vpmethod as vm
import allure


class TestCollections(object):
    driver = WebDriver
    _test_create_collection_set = vm.load_param('TestCollections', 'test_create_collection_set')
    _test_create_collection_set_failed = vm.load_param('TestCollections', 'test_create_collection_set_failed')
    _test_create_collection_failed = vm.load_param('TestCollections', 'test_create_collection_failed')
    # _test_rename_collection = vm.load_param('TestCollections', 'test_rename_collection')
    _test_rename_collection_failed = vm.load_param('TestCollections', 'test_rename_collection_failed')
    _test_rename_collection_set_failed = vm.load_param('TestCollections', 'test_rename_collection_set_failed')

    @classmethod
    def setup_class(cls):
        cls.mainPage = App.main()
        cls.mainPage.driver.maximize_window()

    def setup_method(self):
        self.mainPage = App.main()
        time.sleep(3)

    def teardown_method(self):
        self.mainPage.driver.quit()

    @allure.feature('Prepare')
    def test_random_view_group_sort(self):
        vm.log().debug('CASE: test_random_view_group_sort')
        self.mainPage.selectCollection()
        self.mainPage.changeView('random')
        self.mainPage.changeGroup('random')
        self.mainPage.changeSort('random')

    @allure.feature("Create collection set")
    @pytest.mark.parametrize(('s',), _test_create_collection_set)
    def test_create_collection_set(self, s):
        vm.log().debug('CASE: test_create_collection_set')
        selected_info = self.mainPage.selectFromCollections()
        self.mainPage.rightClick()
        self.mainPage.openCreateCollectionSet()
        created_name = self.mainPage.confirmCreateCollectionSet(s)
        time.sleep(2)
        tables = vm.get_from_db("Select Id from CollectionSets WHERE Name='%s'" % created_name)
        vm.log().debug(tables)
        set_id = tables[-1][0]
        if selected_info[0] == "Collections":
            parent_set_id = vm.get_from_db(
                "select CollectionSetId from JoinCollectionAndCollectionSet where CollectionId=%s" % selected_info[1])
            new_set_parent = vm.get_from_db(
                "select ParentCollectionSetId from JoinCollectionSetAndCollectionSet where ChildCollectionSetId=%s" % set_id)
            vm.log().debug(parent_set_id)
            vm.log().debug(new_set_parent)
            if not parent_set_id:
                assert not new_set_parent
            else:
                assert parent_set_id == new_set_parent
        elif selected_info[0] == "CollectionSets":
            parent_set_id = vm.get_from_db(
                "select ParentCollectionSetId from JoinCollectionSetAndCollectionSet where ChildCollectionSetId=%s" % set_id)[0][0]
            vm.log().debug(parent_set_id)
            assert parent_set_id == selected_info[1]

    @allure.feature("Create collection set")
    def test_cancel_create_collection_set(self):
        vm.log().debug('CASE: test_cancel_create_collection_set')
        self.mainPage.selectFromCollections()
        self.mainPage.rightClick()
        self.mainPage.openCreateCollectionSet()
        self.mainPage.closeCreateCollectionSetDialog()

    @allure.feature("Create collection set")
    @pytest.mark.parametrize(('s', 'm'), _test_create_collection_set_failed)
    def test_create_collection_set_failed(self, s, m):
        vm.log().debug('CASE: test_create_collection_set_failed')
        self.mainPage.selectFromCollections()
        self.mainPage.rightClick()
        self.mainPage.openCreateCollectionSet()
        self.mainPage.confirmCreateCollectionSet(s)
        err = self.mainPage.createCollectionSetError()
        self.mainPage.closeCreateCollectionSetDialog()
        assert (m in err)

    @allure.feature("Create collection")
    def test_create_collection(self):
        vm.log().debug('CASE: test_create_collection')
        selected_info = self.mainPage.selectFromCollections()
        self.mainPage.rightClick()
        self.mainPage.openCreateCollectionDialog()
        created_name = self.mainPage.confirmCreateCollection()
        time.sleep(2)
        collection_id = vm.get_from_db("select Id from Collections where Name='%s'" % created_name)[0][0]
        if selected_info[0] == "Collections":
            parent_set_id = vm.get_from_db(
                "select CollectionSetId from JoinCollectionAndCollectionSet where CollectionId=%s" % selected_info[1])
            new_set_parent = vm.get_from_db(
                "select CollectionSetId from JoinCollectionAndCollectionSet where CollectionId=%s" % collection_id)
            vm.log().debug(parent_set_id)
            vm.log().debug(new_set_parent)
            if not parent_set_id:
                assert not new_set_parent
            else:
                assert parent_set_id == new_set_parent
        elif selected_info[0] == "CollectionSets":
            parent_set_id = vm.get_from_db(
                "select CollectionSetId from JoinCollectionAndCollectionSet where CollectionId=%s" % collection_id)[0][0]
            vm.log().debug(parent_set_id)
            assert parent_set_id == selected_info[1]

    @allure.feature("Create collection")
    def test_create_collection_and_set_as_target(self):
        vm.log().debug('CASE: test_create_collection_and_set_as_target')
        self.mainPage.selectFromCollections()
        self.mainPage.rightClick()
        self.mainPage.openCreateCollectionDialog()
        self.mainPage.checkOnSetAsTarget()
        created_name = self.mainPage.confirmCreateCollection()
        time.sleep(2)
        collection_id = vm.get_from_db("select Id from Collections where Name='%s'" % created_name)[0][0]
        assert str(vm.get_target_id()) == str(collection_id)

    @allure.feature("Create collection")
    def test_cancel_create_collection(self):
        vm.log().debug('CASE: test_cancel_create_collection')
        self.mainPage.selectFromCollections()
        self.mainPage.rightClick()
        self.mainPage.openCreateCollectionDialog()
        self.mainPage.closeCreateCollectionDialog()

    @allure.feature("Create collection")
    @pytest.mark.parametrize(('s', 'm'), _test_create_collection_failed)
    def test_create_collection_failed(self, s, m):
        vm.log().debug('CASE: test_create_collection_failed')
        selected_info = self.mainPage.selectFromCollections()
        self.mainPage.rightClick()
        self.mainPage.openCreateCollectionDialog()
        self.mainPage.confirmCreateCollection(s)
        err = self.mainPage.createCollectionError()
        self.mainPage.closeCreateCollectionDialog()
        assert (m in err)

    @allure.feature("set as target collection")
    def test_set_as_target_collection(self):
        vm.log().debug('CASE: test_set_as_target_collection')
        collection_id = self.mainPage.selectCollection()
        self.mainPage.rightClick()
        self.mainPage.setAsTargetCollection()
        t_id = int(vm.get_target_id())
        assert (collection_id == t_id)

    @allure.feature("move collection/set")
    def test_move_collection(self):
        vm.log().debug('CASE: test_move_collection')
        selected_id = self.mainPage.selectCollection()
        self.mainPage.rightClick()
        target_id = self.mainPage.moveCollection()
        # todo:assert 根据selected_id，找parent id，和target_id一致

    @allure.feature("move collection/set")
    def test_move_collection_set(self):
        vm.log().debug('CASE: test_move_collection_set')
        selected_id = self.mainPage.selectCollectionSet()
        self.mainPage.rightClick()
        target_id = self.mainPage.moveCollectionSet(selected_id)
        # todo:assert 根据selected_id，找parent id，和target_id一致

    @allure.feature("rename")
    def test_rename_collection(self):
        vm.log().debug('CASE: test_rename_collection')
        selected_id = self.mainPage.selectCollection()
        self.mainPage.rightClick()
        self.mainPage.openRenameDialog()
        s = self.mainPage.confirmRename()
        self.mainPage.waitRenameComplete()
        selected_name = vm.get_from_db("select Name from Collections where Id=%s" % selected_id)[0][0]
        assert selected_name == s

    @allure.feature("rename")
    @pytest.mark.parametrize(('s', 'm'), _test_rename_collection_failed)
    def test_rename_collection_failed(self, s, m):
        vm.log().debug('CASE: test_rename_collection_failed')
        selected_id = self.mainPage.selectCollection()
        self.mainPage.rightClick()
        self.mainPage.openRenameDialog()
        self.mainPage.confirmRename(s)
        get_err = self.mainPage.getRenameErr()
        assert (m in get_err)

    @allure.feature("rename")
    def test_rename_collection_set(self):
        vm.log().debug('CASE: test_rename_collection_set')
        selected_id = self.mainPage.selectCollectionSet()
        self.mainPage.rightClick()
        self.mainPage.openRenameCollectionSetDialog()
        s = self.mainPage.confirmRename()
        self.mainPage.waitRenameComplete()
        selected_name = vm.get_from_db("select Name from CollectionSets where Id=%s" % selected_id)[0][0]
        assert selected_name == s

    @allure.feature("rename")
    @pytest.mark.parametrize(('s', 'm'), _test_rename_collection_set_failed)
    def test_rename_collection_set_failed(self, s, m):
        vm.log().debug('CASE: test_rename_collection_set_failed')
        self.mainPage.selectCollectionSet()
        self.mainPage.rightClick()
        self.mainPage.openRenameCollectionSetDialog()
        self.mainPage.confirmRename(s)
        get_err = self.mainPage.getRenameErr()
        assert (m in get_err)

    @allure.feature("remove")
    def test_remove_collection(self):
        vm.log().debug('CASE: test_remove_collection')
        selected_id = self.mainPage.selectCollection()
        self.mainPage.rightClick()
        self.mainPage.removeCollection()
        self.mainPage.WaitProgressDialogClosed()
        table = vm.get_from_db("select Name from Collections where Id=%s" % selected_id)
        assert table == []

    @allure.feature("remove")
    def test_remove_collection_set(self):
        vm.log().debug('CASE: test_remove_collection_set')
        selected_id = self.mainPage.selectCollectionSet()
        vm.log().debug(selected_id)
        self.mainPage.rightClick()
        self.mainPage.removeCollectionSet()
        self.mainPage.WaitProgressDialogClosed()
        table = vm.get_from_db("select Name from CollectionSets where Id=%s" % selected_id)
        assert table == []

    @allure.feature("export")
    @pytest.mark.skip(reason="not implemented")
    def test_export_collections(self):
        vm.log().debug('CASE: test_export_collections')
        pass
